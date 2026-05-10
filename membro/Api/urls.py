from django.urls import path
from . import views

urlpatterns = [
    # ... url lain ...
    path('api/notif/badge/', views.APINotifBadgeMembro.as_view(), name='api-notif-badge'),
    path('api/notif/items/', views.APINotifPediduFounMembro.as_view(), name='api-notif-items'),
]