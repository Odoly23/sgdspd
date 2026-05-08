from django.urls import path
from . import views

urlpatterns=[

    path('api/sexu/', views.APISexu.as_view()),
    path('api/umur/', views.APIUmur.as_view()),
    path('api/estado/', views.APIEstadoCivil.as_view()),
    path('api/sexu-estado/', views.APISexuEstadoCivil.as_view()),
    path('api/tahun/', views.APITahunLahir.as_view()),
    path('api/edukasaun/', views.APIEdukasaun.as_view()),
]
