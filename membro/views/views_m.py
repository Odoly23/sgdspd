import datetime, csv, io, os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from config.decorators import allowed_users
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from membro.forms import MembroForm, ContactInfoForm, LocationTLForm, AddressOriginForm, PhotoUploadForm, FormalEducationForm,\
						EmployeePositionForm
from membro.models import Membru, ContactInfo, LocationTL, AddressOrigin, Photo, FormalEducation, MembroPosition, MembroUser

#create your views here

@login_required
@allowed_users(allowed_roles=['ald'])
def EmpAdd(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		form = MembroForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.created_by=request.user
			instance.save()
			messages.success(request, f'Aumenta ona.')
			return redirect('add-lokation', hashed=instance.hashed)
	else: form = MembroForm()
	context = {
		'form': form,'group':group,
		'title': 'Rejistu Dados Membro', 'legend': 'Rejistu Dados Membro',
		'link_antes': [
			{'link_name':"g-dash",'link_text':"Painel Membro"},
			{'link_name':"add-mem",'link_text':"Rejistu Dados Membro"}
			],
	}
	return render(request, 'Membro/form.html', context)


@login_required
def membro_detail(request, hashed):
    membro = get_object_or_404(Membru, hashed=hashed)
    contact = getattr(membro, 'contactinfo', None)
    location = getattr(membro, 'locationtl', None)
    photo = getattr(membro, 'photo', None)
    position = getattr(membro, 'membroposition', None)
    membrouser = getattr(membro, 'membrouser', None)
    formaleducations = membro.formaleducation.filter(is_active=True).order_by('-educationlevel__name')
    context = {
        'legend': 'Detallu Membro',
        'title': 'Detallu Membro',
        'obj': membro,
        'contact': contact,
        'location': location,
        'photo': photo,
        'position': position,
        'membrouser': membrouser,
        'formaleducations': formaleducations,
        'link_antes': [
            {'link_name': "g-dash", 'link_text': "Painel Membro"},
            {'link_name': 'emp-detail', 'link_text': 'Detallu Membro', 'link_param': membro.hashed}
        ],
    }
    return render(request, 'Membro/detail.html', context)


@login_required
@allowed_users(allowed_roles=['staff', 'admin', 'post','ald'])
def add_Location(request, hashed):
    emp = get_object_or_404(Membru, hashed=hashed)
    objects = LocationTL.objects.filter(membro=emp).first()
    if request.method == 'POST':
    	form = LocationTLForm(request.POST, instance=objects)
    	if form.is_valid():
    		instance = form.save(commit=False)
    		instance.created_by = request.user
    		instance.membro = emp
    		instance.save()
    		messages.success(request, f'Employee address has been updated.')
    		return redirect('emp-detail', hashed=hashed)
    else:
    	form = LocationTLForm(instance=objects)
    context = {
		'form': form, 'emp': emp,
		'title': 'Adisiona Enderesu', 'legend': 'Adisiona Enderesu',
        'link_antes': [
            {'link_name': "g-dash", 'link_text': "Painel Membro"},
            {'link_name': 'add-lokation', 'link_text': 'Adisiona Enderesu', 'link_param': emp.hashed}
        ],
	}
    return render(request, 'Membro/locationform.html', context)