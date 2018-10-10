import pdb
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.db.models import Q, Sum
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from vhc_project import settings
from .models import *


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
            total = fees.aggregate(Sum('amount')).get('amount__sum', 0)
            # pdb.set_trace()
            return render(request, 'fees/pay_fee.html', {'student': student, 'fees': fees, 'total': total})
        else:
            return HttpResponse("Login Failed")

    institutes = Institute.objects.all().values()
    courses = Course.objects.all().values()

    return render(request, 'fees/login.html', {'institutes': institutes, 'courses': courses})


def pay_fee(request):
    return render(request, 'fees/pay_fee.html')

def pay_success(request):
    return HttpResponse('payment Success')


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
