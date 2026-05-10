from django.urls import path
from . import views as v

urlpatterns = [
    # List
    path('membro/users/', v.membro_user_list, name='membro_user_list'),
    # Detail user (reset pw, troka username)
    path('membro/users/<int:membro_id>/detail/', v.membro_user_detail, name='membro_user_detail'),
    # API endpoints (JSON)
    path('membro/users/<int:membro_id>/api/create/',  v.api_create_membro_user, name='api_create_membro_user'),
    path('membro/users/<int:membro_id>/api/password/', v.api_reset_password, name='api_reset_password'),
    path('membro/users/<int:membro_id>/api/username/', v.api_change_username, name='api_change_username'),
    path('membro/users/<int:membro_id>/api/preview/',  v.api_preview_username, name='api_preview_username'),

    path('profil/minhas/hau/.html', v.my_profile, name='my-profile'),


    path('account/', v.AccountUpdate, name='user-account'),
    path('change/password/', v.UserPasswordChangeView.as_view(), name='user-change-password'),
    path('change/password/done/', v.UserPasswordChangeDoneView.as_view(), name='user-change-password-done'),
]