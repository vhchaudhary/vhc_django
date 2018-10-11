import pdb

import paypalrestsdk
from paypalrestsdk import Invoice
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q, Sum
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vhc_project import settings
from .models import *


def create_payment(request):

    pdb.set_trace()

    if request.POST:
        amount = float(request.POST.get('total_amount'))
        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": "AdI02zdsmtJXaow8V5FYGeU9FU7L5R7upFtf4CQIla4KaCgzAvn9c1kbABAMZH_WIvgdP7iYzxU8Dzyo",
            "client_secret": "EKyBWNYOENY4mQrSCMwpV3XIa1ycAVS3SM0C5oObtslWMDaHCSECKkFSmzh9HtYGm3VdTv6OewVfcRcy"})

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/pay_success",
                "cancel_url": "http://localhost:8000/pay_fail"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Fee",
                        "sku": "Fee",
                        "price": amount,
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": amount,
                    "currency": "USD"},
                "description": "This is the payment transaction description."}]})

        if payment.create():
            print("Payment created successfully")

            for link in payment.links:
                if link.rel == "approval_url":
                    # Convert to str to avoid Google App Engine Unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    approval_url = str(link.href)
                    print("Redirect for approval: %s" % (approval_url))
                    return HttpResponseRedirect(approval_url)
        else:
            print(payment.error)


def pay_success(request):
    if request.method == "GET":
        payment = paypalrestsdk.Payment.find(request.GET.get('paymentId'))

        pdb.set_trace()

        # invoice = Invoice({
        #     'merchant_info': {
        #         "email": "default@merchant.com",
        #     },
        #     "billing_info": [{
        #         "email": "example@example.com"
        #     }],
        #     "items": [{
        #         "name": "Widgets",
        #         "quantity": 20,
        #         "unit_price": {
        #             "currency": "USD",
        #             "value": 2
        #         }
        #     }],
        # })
        #
        # response = invoice.create()
        # print(response)

        return HttpResponse('payment Success')


@csrf_exempt
def log_in(request):
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=user_name, password=password)
        # pdb.set_trace()
        if user is not None:
            login(request, user)
            student = Student.objects.get(user=user.id)
            fees = Fee.objects.filter(branch=student.branch).values()
            # pdb.set_trace()
            return render(request, 'fees/pay_fee.html', {'student': student, 'fees': fees})
        else:
            return HttpResponse("Login Failed")

    institutes = Institute.objects.all().values()
    courses = Course.objects.all().values()

    return render(request, 'fees/login.html', {'institutes': institutes, 'courses': courses})


def pay_fee(request):
    return render(request, 'fees/pay_fee.html')


def log_out(request):
    logout(request)
    return render(request, 'fees/login.html')


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

        user = User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        student = Student(user=user, enr_no=enr_no, branch=branch, course=course, address=address, dob=dob)
        user.save()
        student.save()

    return render(request, 'fees/login.html')


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
