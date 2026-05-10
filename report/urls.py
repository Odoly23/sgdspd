from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard/Tabular/membru.html/', views.dash, name='t-dash'),
    path('relatoriu/', views.report_menu, name='report-menu'),
    path('relatoriu/geral/', views.report_geral, name='report-geral'),
    path('relatoriu/posisaun/', views.report_posisaun, name='report-posisaun'),
    path('relatoriu/status/', views.report_status, name='report-status'),

    # urls.py
    path('lista/<str:sex>/<int:loc_id>/',      views.lista_membro,      name='lista-membru'),
    path('dash/export/',                       views.dash,              name='dash-export'),
]