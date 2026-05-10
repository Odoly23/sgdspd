from django.urls import path
from . import views

urlpatterns = [
    path('Dashboard/membru/', views.dash_mem, name='g-dash'),
    path('Rejistu/membru/', views.EmpAdd, name='add-mem'),
    path('Rejistu/position/membru/<str:hashed>/.html/', views.add_position, name='add-position'),
    path('Rejistu/edukasaun/membru/<str:hashed>/.html/', views.add_education, name='add-edus'),
    path('Rejistu/contact/membru/<str:hashed>/.html/', views.add_contact, name='add-contact'),
    path('membro/detallu/<str:hashed>/', views.membro_detail, name='emp-detail'),
    path('membru/<str:hashed>/location/', views.add_Location, name='add-lokation'),
    path('lista-membru/<str:tipu>/<int:pk>/', views.lista_membru, name='lista-membru'),
    path('update/<str:hashed>/photo/', views.PhotoUpdate, name="photo-update"),
    path('lista-geral/', views.lista_geral_membru, name='lista-geral'),

    #konfirmasaun
    path('list/pending-conf/',  views.list_pending_conf, name='list-pending-conf'),
    path('list/pending-appr/',  views.list_pending_appr, name='list-pending-appr'),

    # ── Aksi Konfirma & Aprova ──
    path('konfirma/<str:hashed>/', views.konfirma_membro, name='konfirma-membro'),
    path('aprova/<str:hashed>/',   views.aprova_membro,   name='aprova-membro'),

]