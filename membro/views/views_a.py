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
from django.http import HttpResponseForbidden

@login_required
@allowed_users(allowed_roles=['staff','postu','admin','ald','suku'])
def dash_mem(request):
    from django.core.paginator import Paginator  # pastikan sudah import di atas file

    group    = request.user.groups.all()[0].name
    user_mem = c_user_mem(request.user)

    loc = None
    if user_mem:
        loc = LocationTL.objects.select_related('village', 'aldeia').filter(membro=user_mem).first()

    data        = []
    nama_lokasi = "LOKASAUN"

    if group in ["postu", "admin", "staff"]:
        data        = list(Village.objects.all().order_by('name'))
        nama_lokasi = "POSTO DOM-ALEIXO"
    elif group == 'suku':
        if loc and loc.village:
            data        = list(SubVillage.objects.filter(village=loc.village).order_by('name'))
            nama_lokasi = f"SUCO {loc.village.name}"
    elif group == 'ald':
        if loc and loc.aldeia:
            data        = [loc.aldeia]
            nama_lokasi = f"ALDEIA {loc.aldeia.name}"

    # ── Build semua data ──
    all_objects = []
    total_mane = total_feto = total_all = 0

    for d in data:
        if isinstance(d, Village):
            male   = LocationTL.objects.filter(village=d, membro__sex="Mane").count()
            female = LocationTL.objects.filter(village=d, membro__sex="Feto").count()
            tipe   = "Suku"
        else:
            male   = LocationTL.objects.filter(aldeia=d, membro__sex="Mane").count()
            female = LocationTL.objects.filter(aldeia=d, membro__sex="Feto").count()
            tipe   = "Aldeia"

        total = male + female
        all_objects.append({
            "id": d.id, "nama": d.name, "tipe": tipe,
            "male": male, "female": female, "total": total
        })
        total_mane += male
        total_feto += female
        total_all  += total

    # ── Paginator 10 per halaman ──
    paginator = Paginator(all_objects, 10)
    page_obj  = paginator.get_page(request.GET.get('page'))

    context = {
        "title":       "Painel Geral Membro",
        "legend":      "Painel Geral Membro",
        "homeactive":  "active",
        "objects1":    page_obj,   # ← pakai page_obj
        "page_obj":    page_obj,   # ← untuk paginator di template
        "group":       group,
        "nama_lokasi": nama_lokasi,
        "total_mane":  total_mane,
        "total_feto":  total_feto,
        "total_all":   total_all,
    }
    return render(request, 'Membro/sumario.html', context)
    
@login_required
@allowed_users(allowed_roles=['staff','postu','admin','ald','suku'])
def lista_membruss(request, tipu, pk):
    group = request.user.groups.all()[0].name
    membros = Membru.objects.none()
    title = ""
    if group in ['postu', 'admin', 'staff']:
        village = Village.objects.get(id=pk)
        lokasi = LocationTL.objects.filter(village=village)
        if tipu == 'mane':
            lokasi = lokasi.filter(membro__sex='Mane')
            title = f"Lista Mane - {village.name}"
        elif tipu == 'feto':
            lokasi = lokasi.filter(membro__sex='Feto')
            title = f"Lista Feto - {village.name}"
        else:
            title = f"Lista Geral - {village.name}"
        membros = Membru.objects.filter(
            id__in=lokasi.values_list('membro_id', flat=True)
        )
    else:
        aldeia = SubVillage.objects.get(id=pk)
        lokasi = LocationTL.objects.filter(aldeia=aldeia)
        if tipu == 'mane':
            lokasi = lokasi.filter(membro__sex='Mane')
            title = f"Lista Mane - {aldeia.name}"
        elif tipu == 'feto':
            lokasi = lokasi.filter(membro__sex='Feto')
            title = f"Lista Feto - {aldeia.name}"
        else:
            title = f"Lista Geral - {aldeia.name}"
        membros = Membru.objects.filter(
            id__in=lokasi.values_list('membro_id', flat=True)
        )
    context = {
        'title': title,
        'membros': membros,
    }
    return render(request, 'Membro/lista_membru.html', context)


@login_required
@allowed_users(allowed_roles=['staff','postu','admin','ald','suku'])
def lista_geral_membru(request):
    group = request.user.groups.all()[0].name
    membros = Membru.objects.select_related('locationtl').all()
    user_mem = c_user_mem(request.user)
    loc = None
    if user_mem:
        loc = LocationTL.objects.filter(membro=user_mem).first()
    estrutura = "POSTO DOM-ALEIXO"
    if group in ['admin', 'staff', 'postu']:
        membros = membros.order_by('name')
    elif group == 'suku':
        if loc and loc.village:
            membros = membros.filter(locationtl__village=loc.village)
            estrutura = f"SUCO {loc.village.name}"
    elif group == 'ald':
        if loc and loc.aldeia:
            membros = membros.filter(locationtl__aldeia=loc.aldeia)
            estrutura = f"ALDEIA {loc.aldeia.name}"
    context = {
        'title': 'Lista Geral Membru',
        'membros': membros,
        'group': group,
        'estrutura': estrutura,
    }

    return render(request,'Membro/lista_geral.html', context)

@login_required
@allowed_users(allowed_roles=['staff', 'postu', 'admin', 'ald', 'suku'])
def lista_membru(request, pk, tipu):
    group = request.user.groups.all()[0].name

    user_mem = c_user_mem(request.user)
    loc = None
    if user_mem:
        loc = LocationTL.objects.select_related('village', 'aldeia').filter(membro=user_mem).first()

    locations = LocationTL.objects.select_related(
        'aldeia',
        'membro',
        'membro__membroposition__position'
    )

    if group in ["postu", "admin", "staff"]:
        # pk = Village.id
        village = get_object_or_404(Village, pk=pk)
        locations = locations.filter(village=village)
        nama_lokasi = village.name

    elif group == 'suku':
        # pk = SubVillage(Aldeia).id
        aldeia = get_object_or_404(SubVillage, pk=pk)
        village = aldeia.village
        locations = locations.filter(aldeia=aldeia)
        nama_lokasi = aldeia.name

    elif group == 'ald':
        # pk = Aldeia.id (sama dengan loc.aldeia)
        aldeia = get_object_or_404(SubVillage, pk=pk)
        village = aldeia.village
        locations = locations.filter(aldeia=aldeia)
        nama_lokasi = aldeia.name

    else:
        return HttpResponseForbidden("Akses ditolak.")

    # Filter tipu
    if tipu == 'mane':
        locations = locations.filter(membro__sex='Mane')
        title = f"Lista Mane - {nama_lokasi}"
    elif tipu == 'feto':
        locations = locations.filter(membro__sex='Feto')
        title = f"Lista Feto - {nama_lokasi}"
    else:
        title = f"Lista Geral - {nama_lokasi}"

    # Kelompokkan per aldeia
    grouped = {}
    total_rows = 0
    for loc_item in locations:
        aldeia_name = loc_item.aldeia.name if loc_item.aldeia else "-"
        try:
            position = loc_item.membro.membroposition.position.name
        except:
            position = "-"
        name = loc_item.membro.name
        if aldeia_name not in grouped:
            grouped[aldeia_name] = []
        grouped[aldeia_name].append({
            "position": position,
            "name": name,
        })
        total_rows += 1

    data = []
    for aldeia_name, rows in grouped.items():
        data.append({
            "aldeia": aldeia_name,
            "rows": rows,
            "rowspan": len(rows)
        })

    context = {
        "title": title,
        "legend": title,
        "homeactive": "active",
        "village": village,
        "data": data,
        "total_rows": total_rows,
        "group": group,
        "nama_lokasi": nama_lokasi,
    }
    return render(request, 'Membro/sum2.html', context)