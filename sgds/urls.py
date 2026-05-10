"""
URL configuration for sgds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500
from main.views import logout_view, loginPage
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', loginPage, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', include('main.urls')),
    path('Membru/', include('membro.urls')),
    path('custom/', include('custom.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('API/Report/', include('report.Api.urls')),
    path('API/Membru/', include('membro.Api.urls')),
    path('Utilizadores/', include('user.urls')),
    path('Sumario/', include('report.urls')),
    path('reset-password/', auth_views.PasswordResetView.as_view( template_name='auth/password_reset.html', email_template_name='registration/password_reset_email.html'),name='password_reset'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "SISTEMA GESTAUN DADOS PD-PADA - SUPER USER"
admin.site.site_title = "SISTEMA GESTAUN DADOS PD-PADA - SUPER USER"
admin.site.index_title = "Portal Super User"

handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'