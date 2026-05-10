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


@login_required
@allowed_users(allowed_roles=['suku'])
def list_pending_conf(request):
    try:
        village = request.user.membrouser.membro.locationtl.village
        objects = Membru.objects.filter(
            locationtl__village=village,
            is_conf=False
        ).order_by('-created_at')
    except Exception:
        objects = Membru.objects.none()

    context = {
        'objects': objects,
        'title': 'Lista Membro Seidauk Konfirma',
        'legend': 'Lista Membro Seidauk Konfirma',
    }
    return render(request, 'Notif/list_pending.html', context)


@login_required
@allowed_users(allowed_roles=['postu'])
def list_pending_appr(request):
    objects = Membru.objects.filter(
        is_conf=True,
        is_appr=False
    ).order_by('-created_at')

    context = {
        'objects': objects,
        'title': 'Lista Membro Seidauk Aprova',
        'legend': 'Lista Membro Seidauk Aprova',
    }
    return render(request, 'Notif/list_pending.html', context)


@login_required
@allowed_users(allowed_roles=['suku'])
def konfirma_membro(request, hashed):
    import datetime
    emp = get_object_or_404(Membru, hashed=hashed)

    if request.method == 'POST':
        emp.is_conf = True
        emp.date_conf = datetime.date.today()
        emp.conf_by = request.user
        emp.save()
        messages.success(request, f'{emp.name} konfirmadu ona.')
        return redirect('list-pending-conf')

    context = {
        'obj': emp,
        'title': 'Konfirma Membro',
        'legend': 'Konfirma Membro',
    }
    return render(request, 'Notif/konfirma.html', context)


@login_required
@allowed_users(allowed_roles=['postu'])
def aprova_membro(request, hashed):
    emp = get_object_or_404(Membru, hashed=hashed)
    if request.method == 'POST':
        emp.is_appr = True
        emp.date_appr = datetime.date.today()
        emp.appr_by = request.user
        emp.save()
        messages.success(request, f'{emp.name} aprovadu ona.')
        return redirect('list-pending-appr')

    context = {
        'obj': emp,
        'title': 'Aprova Membro',
        'legend': 'Aprova Membro',
    }
    return render(request, 'Notif/aprova.html', context)