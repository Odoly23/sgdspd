from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from custom.models import  Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram, \
                           Year, Estructure
from django.contrib.auth import authenticate,login,logout
from user.models import AuditLogin
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.contrib import messages
from urllib.parse import urlparse
from django.urls import resolve
from membro.models import Membru, LocationTL
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User,Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
#from ipware import get_client_ip
#from ip2geotools.databases.noncommercial import DbIpCity

# Create your views here.
@login_required
def home(request):
    group = request.user.groups.all()[0].name
    context = {
        #'group':group,
        "title": "Sistema Manajemento Dadus Partido Democrático ",
        'homeactive':"active",
    }
    return render(request, 'home/home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            AuditLogin.objects.create(user=request.user)
            messages.success(request, f'Bemvido, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Username Ou password salah. Favor koko Fila Fali.')

    return render(request, 'auth/login.html', {"title": "Pajina Login",})



@login_required
def logout_view(request):
    request.session.flush()
    logout(request)
    return render(request, 'auth/logout.html')

def error_404(request, exception):
        data = {}
        return render(request,'auth/404.html', data)

def error_500(request):
        data = {}
        return render(request,'auth/500.html', data)