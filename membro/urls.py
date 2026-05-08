from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard/membru/', views.dash_mem, name='g-dash'),
    path('Rejistu/membru/', views.EmpAdd, name='add-mem'),
    path('membro/detallu/<str:hashed>/', views.membro_detail, name='emp-detail'),
    path('membru/<str:hashed>/location/', views.add_Location, name='add-lokation'),
    path('lista-membru/<str:tipu>/<int:pk>/', views.lista_membru, name='lista-membru'),
    
    path('lista-geral/', views.lista_geral_membru, name='lista-geral'),
]