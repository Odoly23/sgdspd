import csv, io, datetime
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from custom.models import  Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram, \
                           Year, Estructure
from membro.models import (
    Membru, ContactInfo, LocationTL, AddressOrigin,
    Photo, FormalEducation, MembroUser, MembroPosition
)
from django.db.models.functions import ExtractYear  


# Create your views here.
def get_filtered_queryset(request):
    group = request.user.groups.all()[0].name
    qs = Membru.objects.all()
    user_mem = None
    loc = None
    try:
        user_mem = MembroUser.objects.get(user=request.user).membro
        loc = LocationTL.objects.filter(membro=user_mem).first()
    except:
        pass
    if group in ['admin', 'staff', 'postu']:
        return qs
    elif group == 'suku':
        if loc and loc.village:
            return qs.filter(locationtl__village=loc.village)
    elif group == 'ald':
        if loc and loc.aldeia:
            return qs.filter(locationtl__aldeia=loc.aldeia)
    return qs.none()


class APIMun(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        data = []
        muns = Municipality.objects.all()
        for m in muns:
            total = LocationTL.objects.filter(municipality=m).count()
            data.append({
                "name": m.name,
                "hc-key": m.hckey,  
                "value": total
            })

        return Response(data)

class APISexu(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = get_filtered_queryset(request)
        data = (qs.values('sex').annotate(total=Count('id')))
        label = [d['sex'] or 'La Hatene' for d in data]
        obj = [d['total'] for d in data]
        return Response({
            'label': label,
            'obj': obj
        })

class APIUmur(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = get_filtered_queryset(request)
        today = datetime.date.today()
        def get_date(years):
            try:
                return today.replace(year=today.year - years)
            except ValueError:
                return today.replace(month=2, day=28, year=today.year - years)
        groups = {
            '0-17': Q(dob__gt=get_date(18)),
            '18-30': Q(dob__lte=get_date(18)) & Q(dob__gt=get_date(31)),
            '31-45': Q(dob__lte=get_date(31)) & Q(dob__gt=get_date(46)),
            '46-60': Q(dob__lte=get_date(46)) & Q(dob__gt=get_date(61)),
            '60+': Q(dob__lte=get_date(61)),
        }

        label = []
        obj = []
        for name, condition in groups.items():
            count = qs.filter( dob__isnull=False).filter(condition).count()
            label.append(name)
            obj.append(count)
        return Response({
            'label': label,
            'obj': obj
        })

class APIEstadoCivil(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = get_filtered_queryset(request)
        data = (qs.values('marital').annotate(total=Count('id')))
        label = [d['marital'] or '-' for d in data]
        obj = [d['total'] for d in data]
        return Response({
            'label': label,
            'obj': obj
        })

class APISexuEstadoCivil(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = get_filtered_queryset(request)
        marital_choices = [
            'Solteiro/a',
            'Casado/a',
            'Divorciado/a',
            'Viuvo/a'
        ]
        mane_data = []
        feto_data = []
        for m in marital_choices:
            mane_data.append(qs.filter(sex='Mane', marital=m).count())
            feto_data.append(qs.filter(sex='Feto', marital=m).count())
        return Response({
            'label': marital_choices,
            'mane': mane_data,
            'feto': feto_data,
        })

class APITahunLahir(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = get_filtered_queryset(request)
        results = (
            qs.filter(dob__isnull=False)
            .annotate(tahun=ExtractYear('dob'))
            .values('tahun')
            .annotate(total=Count('id'))
            .order_by('tahun')
        )
        label = [str(r['tahun']) for r in results]
        obj = [r['total'] for r in results]
        return Response({
            'label': label,
            'obj': obj
        })


class APIEdukasaun(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        qs = get_filtered_queryset(request)
        edu_levels = EducationLevel.objects.all()
        labels = []
        obj = []
        for edu in edu_levels:
            total = FormalEducation.objects.filter(
                membro__in=qs,
                educationlevel=edu
            ).count()
            labels.append(edu.name)
            obj.append(total)
        return Response({
            'label': labels,
            'obj': obj
        }) 
class APISumariuSuku(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        labels = []
        data_ativu = []
        data_la_ativu = []
        data_mate = []
        
        villages = Village.objects.all()
        
        for v in villages:
            labels.append(v.name)
            data_ativu.append(LocationTL.objects.filter(village=v, employee__status__name="Ativu").count())
            data_la_ativu.append(LocationTL.objects.filter(village=v, employee__status__name="La Ativu").count())
            data_mate.append(LocationTL.objects.filter(village=v, employee__status__name="Mate").count())
            
        data = {
            'labels': labels,
            'ativu': data_ativu,
            'la_ativu': data_la_ativu,
            'mate': data_mate,
        }
        return Response(data)





class APISumariuSukuTahun(APIView):
    def get(self, request, format=None):
        latest = Membru.objects.order_by('-datetime').first()
        tinan = latest.datetime.year if latest else 2024
        
        villages = Village.objects.all()
        
        data_ativu = []
        data_la_ativu = []
        data_mate = []
        labels_suku = []

        for suku in villages:
            base = LocationTL.objects.filter(village=suku, employee__datetime__year=tinan)
            
            c_ativu = base.filter(employee__status__name="Ativu").count()
            c_la_ativu = base.filter(employee__status__name="La Ativu").count()
            c_mate = base.filter(employee__status__name="Mate").count()

     
            if (c_ativu + c_la_ativu + c_mate) > 0:
                labels_suku.append(suku.name)
                data_ativu.append(c_ativu)
                data_la_ativu.append(c_la_ativu)
                data_mate.append(c_mate)

        datasets = [
            {
                'label': 'Ativu',
                'data': data_ativu,
                'backgroundColor': '#378ADD', 
            },
            {
                'label': 'La Ativu',
                'data': data_la_ativu,
                'backgroundColor': '#ffc107',
            },
            {
                'label': 'Mate',
                'data': data_mate,
                'backgroundColor': '#dc3545', 
            }
        ]

        return Response({
            'tinan': tinan,
            'labels': labels_suku, 
            'datasets': datasets
        })




class APIEdukasaunSuku(APIView):
    def get(self, request, format=None):
        edu_levels = EducationLevel.objects.all()
        villages = Village.objects.annotate(
            total=Count('locationtl')
        ).filter(total__gt=0).order_by('-total')

        labels = [v.name for v in villages]
        datasets = []
        colors = ['#378ADD', '#D4537E', '#198754', '#ffc107', '#dc3545', '#6f42c1']

        for i, edu in enumerate(edu_levels):
            data_counts = []
            for v in villages:
                count = FormalEducation.objects.filter(
                    educationlevel=edu,
                    employee__locationtl__village=v
                ).count()
                data_counts.append(count)
            if sum(data_counts) > 0:
                datasets.append({
                    'label': edu.name,
                    'data': data_counts,
                    'backgroundColor': colors[i % len(colors)]
                })

        return Response({
            'labels': labels, 
            'datasets': datasets 
        })
