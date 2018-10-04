import pdb
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from polls.models import Person
from .forms import PersonForm

# Create your views here.

def index(reqeust):
    # pdb.set_trace()
    return HttpResponse('HEllo vhc.........')


def register(request):
    form = PersonForm()
    return render(request, 'polls/register.html', {'form':form})


def user_data(request):
    return render(request, 'polls/user_data.html', {'persons': Person.objects.all})


def create_person(request):

    if request.is_ajax() and request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        bld_grp = request.POST.get('bldgroup')

        rec = Person(name=name, email=email, address=address, mobile=mobile, gender=gender, dob=dob, bld_group=bld_grp)
        rec.save()

        json_data = {'id': rec.id, 'name': rec.name, 'email': rec.email, 'address': rec.address,
                     'mobile': rec.mobile, 'gender': rec.gender, 'dob': rec.dob, 'bld_group': rec.bld_group}

        return JsonResponse(json_data)

    # pdb.set_trace()


@csrf_exempt
def delete_person(request):
    if request.method == 'POST':
        rec = Person.objects.get(pk=int(request.POST.get('id')))
        rec.delete()

        return JsonResponse({'success': True})

    return render(request, 'polls/user_data.html', {'persons': Person.objects.all})


@csrf_exempt
def update_person(request):
    if request.is_ajax() and request.method == 'POST':
        if request.POST.get('req_type') == 'get_update_data':
            rec = Person.objects.get(pk=int(request.POST.get('id')))
            json_data = {'id': rec.id, 'name': rec.name, 'email': rec.email, 'address': rec.address,
                         'mobile': rec.mobile, 'gender': rec.gender, 'dob': rec.dob, 'bld_group': rec.bld_group}
            return JsonResponse(json_data)

        else:

            rec = Person.objects.get(pk=int(request.POST.get('rec_id')))

            rec.name = request.POST.get('name')
            rec.email = request.POST.get('email')
            rec.address = request.POST.get('address')
            rec.mobile = request.POST.get('mobile')
            rec.gender = request.POST.get('gender')
            rec.dob = request.POST.get('dob')
            rec.bld_group = request.POST.get('bldgroup')

            json_data = {'id': rec.id, 'name': rec.name, 'email': rec.email, 'address': rec.address,
                         'mobile': rec.mobile, 'gender': rec.gender, 'dob': rec.dob, 'bld_group': rec.bld_group}

            rec.save()

            return JsonResponse(json_data)

    return render(request, 'polls/user_data.html', {'persons': Person.objects.all})
