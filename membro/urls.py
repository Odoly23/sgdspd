from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/membru/', views.dash_mem, name='g-dash'),
]