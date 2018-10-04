import pdb

from django.http import JsonResponse
from django.shortcuts import render
from . models import *


def login(reqeust):

    institutes = Institute.objects.all()

    return render(reqeust, 'fees/login.html', {'institutes': institutes})


def get_branches(request):

    if request.method == 'POST':

        if request.POST.get('id'):
            branches = Branch.objects.filter(institute=int(request.POST['id']))

        # pdb.set_trace()

        json_data = {'branches': [b.name for b in branches]}
        return JsonResponse(json_data)