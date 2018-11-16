import logging
import paypalrestsdk
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q, Sum
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vhc_project import settings
from . models import *
from decouple import config


def create_payment(request):

    if request.POST:
        amount = request.POST.get('total_amount')

        if amount:
            paypalrestsdk.configure({
                "mode": "sandbox",  # sandbox or live
                "client_id": config('client_id', default=''),
                "client_secret": config('client_secret', default='')})

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": "http://127.0.0.1:8000/pay_done",
                    "cancel_url": "http://127.0.0.1:8000/pay_fail"},
                "transactions": [{"item_list": {
                        "items": [{
                            "name": "Education Fee",
                            "sku": "Fee",
                            "price": amount,
                            "currency": "USD",
                            "quantity": 1}]},
                    "amount": {"total": amount, "currency": "USD"},
                    "description": "This is the payment transaction description."}]})

            if payment.create():
                logging.info("Payment created successfully")

                for link in payment.links:
                    if link.rel == "approval_url":
                        # Convert to str to avoid Google App Engine Unicode issue
                        # https://github.com/paypal/rest-api-sdk-python/pull/58
                        approval_url = str(link.href)
                        logging.info("Redirect for approval: %s" % (approval_url))
                        return HttpResponseRedirect(approval_url)
            else:
                logging.error(payment.error)
        else:
            logging.error("Invalid Amount...")


def get_amount(request):
    
    if request.method == "POST" and request.is_ajax():
        branch_ids = dict(request.POST).get('ids[]', False)

        try:
            total_amount = Fee.objects.filter(pk__in=branch_ids).aggregate(Sum('amount')).get('amount__sum')
        except TypeError:
            return JsonResponse({'amount': False})

        return JsonResponse({'amount': total_amount})


def payment_done(request):
    if request.method == "GET":

        payment = paypalrestsdk.Payment.find(request.GET.get('paymentId'))
        payer_id = payment.payer.payer_info.payer_id

        if payment.execute({"payer_id": payer_id}):
            print("Payment execute successfully")
        else:
            print(payment.error)

        tr = Transaction(uuid=payment.id, user=User.objects.get(pk=int(request.user.id)), status='completed',
                         paid_amount=float(payment.transactions[0].amount.total))
        tr.save()

        vals = {}
        if payment:
            vals.update({'id': payment.id,
                         'payer': payment.payer.payer_info.email,
                         'merchant': payment.transactions[0].payee.merchant_id,
                         'amount': payment.transactions[0].amount.total,
                         'date': payment.create_time})


        return render(request, 'fees/pay_done.html', {'vals': vals})


@csrf_exempt
def log_in(request):

    # tasks.shared_task_test.delay(1000)

    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            student = Student.objects.get(user=user.id)
            fees = Fee.objects.filter(branch=student.branch).values()
            return render(request, 'fees/pay_fee.html', {'student': student, 'fees': fees})
        else:
            return HttpResponse("Login Failed")

    institutes = Institute.objects.all().values()
    courses = Course.objects.all().values()

    return render(request, 'fees/login.html', {'institutes': institutes, 'courses': courses})


def log_out(request):
    logout(request)

    institutes = Institute.objects.all().values()
    courses = Course.objects.all().values()

    return render(request, 'fees/login.html', {'institutes': institutes, 'courses': courses})


def get_branches(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            branches = Branch.objects.filter(institute=int(request.POST['id']))
        json_data = {'branches': {b.id: b.name for b in branches}}
        return JsonResponse(json_data)


def forgot_password(request):
    return render(request, 'fees/forgot_password.html')


def send_pass_reset_mail(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST.get('username')

        try:
            user = User.objects.get(Q(username=name) | Q(email=name))
            email_msg = "This is test message for reset password"
            email = EmailMessage("Reset Password", email_msg, settings.EMAIL_HOST_USER, [user.email])
            email.send()

            return JsonResponse({'success': True})

        except User.DoesNotExist:
            return JsonResponse({'success': False})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('c_password')
        enr_no = request.POST.get('enr_no')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        branch = Branch.objects.get(pk=int(request.POST.get('branch')))
        course = Course.objects.get(pk=int(request.POST.get('course')))
        address = request.POST.get('address')
        dob = request.POST.get('dob')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=fname,
                                        last_name=lname)
        student = Student(user=user, enr_no=enr_no, branch=branch, course=course, address=address, dob=dob)
        user.save()
        student.save()

    return render(request, 'fees/login.html')
