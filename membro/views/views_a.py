import hashlib, uuid, os, datetime
from django.http import Http404
from django.utils import timezone
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from custom.models import  Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram, \
                           Year, Estructure
from django.template.loader import render_to_string
from django.contrib import messages
from membro.models import Membru, LocationTL, ContactInfo, AddressOrigin, MembroPosition

from django.db.models import Count, Sum, Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User,Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config.decorators import allowed_users
from config.auth_utils import c_user_mem

@login_required
@allowed_users(allowed_roles=['staff','postu','admin','ald','suku'])
def dash_mem(request):
    group = request.user.groups.all()[0].name
    objects1 = []
    user_mem = c_user_mem(request.user)
    loc = None
    if user_mem:
        loc = LocationTL.objects.select_related('village', 'aldeia').filter(membro=user_mem).first()
    data = []
    if group == "postu" or group == "admin" or group == "staff":
        data = list(Village.objects.all())
        nama_lokasi = "POSTO DOM-ALEIXO"
    elif group == 'suku':
        if loc and loc.village:
            data = list(SubVillage.objects.filter(village=loc.village))
            nama_lokasi = f"SUCO {loc.village.name}"
        else:
            nama_lokasi = "SUCO"
    elif group == 'ald':
        if loc and loc.aldeia:
            data = [loc.aldeia]
            nama_lokasi = f"ALDEIA {loc.aldeia.name}"
        else:
            nama_lokasi = "ALDEIA"
    else:
        nama_lokasi = "LOKASAUN"
    for d in data:
        if isinstance(d, Village):
            male = LocationTL.objects.filter(village=d, membro__sex="Mane").count()
            female = LocationTL.objects.filter(village=d, membro__sex="Feto").count()
            tipe = "Suku"
        else:
            male = LocationTL.objects.filter( aldeia=d, membro__sex="Mane").count()
            female = LocationTL.objects.filter(aldeia=d, membro__sex="Feto").count()
            tipe = "Aldeia"
        total = male + female
        objects1.append({"id": d.id, "nama": d.name,"tipe": tipe,"male": male,"female": female,"total": total})
    context = {
        "title": "Painel Geral Membro",
        "legend": "Painel Geral Membro",
        "homeactive": "active",
        "objects1": objects1,
        "group": group,
        "nama_lokasi": nama_lokasi,
    }
    return render(request, 'Membro/sumario.html', context)
