import pdb
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from . models import *


def log_in(request):

    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=user_name, password=password)
        # pdb.set_trace()
        if user is not None:
            login(request, user)
            return HttpResponse("Login Success")
        else:
            return HttpResponse("Login Failed")


    institutes = Institute.objects.all().values()
    courses = Course.objects.all().values()

    return render(request, 'fees/login.html', {'institutes': institutes, 'courses':courses})


def log_out(request):
    logout(request)


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

        user = Student.objects.create_user(username=username, email=email, password=password, enr_no=enr_no, first_name=fname,
                                                last_name=lname, branch=branch, course=course, address=address, dob=dob)
        # pdb.set_trace()
        user.save()

    return render(request, 'fees/login.html')


def get_branches(request):
    if request.method == 'POST':
        if request.POST.get('id'):
            branches = Branch.objects.filter(institute=int(request.POST['id']))
        json_data = {'branches': {b.id:b.name for b in branches}}
        return JsonResponse(json_data)