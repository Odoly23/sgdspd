import json
import hashlib
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from membro.models import Membru, MembroUser, MembroPosition, Photo, ContactInfo, LocationTL, FormalEducation
from config.auth_utils import c_user_mem
from user.forms import UserForm, ChangePasswordForm

ESTRUTURA_GROUP_MAP = {
    'AL': 'ald',
    'SK': 'suku',
    'PA': 'postu',
    'MN': 'staff',
}

def _build_username(membro: Membru) -> str:
    first_word = (membro.name or '').strip().split()[0].lower() if membro.name else 'user'
    base = f'{first_word}@#pada'
    if User.objects.filter(username=base).exists():
        return f'{base}.{membro.id}'
    return base


def _parse_name(full_name: str):
    names = (full_name or '').strip().split()
    return (names[0] if names else '', ' '.join(names[1:]) if len(names) > 1 else '')



@login_required
def membro_user_list(request):
    membros = (Membru.objects.select_related('membroposition__estructure','membrouser__user',).filter(membroposition__estructure__code__in=['PA', 'SK', 'AL']).order_by('name'))
    groups      = Group.objects.filter(name__in=['ald', 'suku', 'postu', 'staff'])
    groups_json = json.dumps([{'id': g.id, 'name': g.name} for g in groups])
    context =  {
        'membros':     membros,
        'groups':      groups,
        'groups_json': groups_json,
    }
    return render(request, 'users/list.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# 2. DETAIL USER — reset password & ganti username
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def membro_user_detail(request, membro_id: int):
    """Halaman detail user: tampilkan info, form reset password & ganti username."""
    membro      = get_object_or_404(Membru, pk=membro_id)
    membro_user = get_object_or_404(MembroUser, membro=membro)
    user        = membro_user.user

    return render(request, 'users/detail.html', {
        'membro': membro,
        'user':   user,
    })


# ─────────────────────────────────────────────────────────────────────────────
# 3. API — Buat User (dari modal, terima JSON)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_POST
@transaction.atomic
def api_create_membro_user(request, membro_id: int):
    """
    POST JSON: { "username": "...", "group_id": 3 }
    Buat Django User, assign group, hubungkan ke Membro.
    """
    membro = get_object_or_404(Membru, pk=membro_id)

    if hasattr(membro, 'membrouser'):
        return JsonResponse({'ok': False, 'error': 'Membro já iha konta.'}, status=400)

    try:
        body     = json.loads(request.body)
        username = (body.get('username') or '').strip()
        group_id = body.get('group_id')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'ok': False, 'error': 'Payload inválidu.'}, status=400)

    if not username:
        return JsonResponse({'ok': False, 'error': 'Username la bele mamuk.'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'ok': False, 'error': f'Username "{username}" ona iha.'}, status=400)

    first_name, last_name = _parse_name(membro.name)

    user = User(
        username   = username,
        password   = make_password('pada@#2026'),
        first_name = first_name,
        last_name  = last_name,
        is_active  = True,
    )
    user.save()

    group_name = None
    if group_id:
        try:
            group = Group.objects.get(pk=group_id)
            user.groups.add(group)
            group_name = group.name
        except Group.DoesNotExist:
            pass

    MembroUser.objects.create(user=user, membro=membro)

    return JsonResponse({
        'ok':        True,
        'username':  user.username,
        'group':     group_name,
        'membro_id': membro.id,
    })


# ─────────────────────────────────────────────────────────────────────────────
# 4. API — Reset Password
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_POST
@transaction.atomic
def api_reset_password(request, membro_id: int):
    """
    POST JSON: { "new_password": "..." }
    Reset password user ke nilai baru.
    """
    membro      = get_object_or_404(Membru, pk=membro_id)
    membro_user = get_object_or_404(MembroUser, membro=membro)

    try:
        body         = json.loads(request.body)
        new_password = (body.get('new_password') or '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'ok': False, 'error': 'Payload inválidu.'}, status=400)

    if not new_password or len(new_password) < 6:
        return JsonResponse({'ok': False, 'error': 'Password minimu 6 karakter.'}, status=400)

    membro_user.user.password = make_password(new_password)
    membro_user.user.save(update_fields=['password'])

    return JsonResponse({'ok': True})


# ─────────────────────────────────────────────────────────────────────────────
# 5. API — Ganti Username
# ─────────────────────────────────────────────────────────────────────────────

@login_required
@require_POST
@transaction.atomic
def api_change_username(request, membro_id: int):
    """
    POST JSON: { "new_username": "..." }
    Ganti username user.
    """
    membro      = get_object_or_404(Membru, pk=membro_id)
    membro_user = get_object_or_404(MembroUser, membro=membro)

    try:
        body         = json.loads(request.body)
        new_username = (body.get('new_username') or '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'ok': False, 'error': 'Payload inválidu.'}, status=400)

    if not new_username:
        return JsonResponse({'ok': False, 'error': 'Username la bele mamuk.'}, status=400)

    if User.objects.filter(username=new_username).exclude(pk=membro_user.user.pk).exists():
        return JsonResponse({'ok': False, 'error': f'Username "{new_username}" ona iha.'}, status=400)

    membro_user.user.username = new_username
    membro_user.user.save(update_fields=['username'])

    return JsonResponse({'ok': True, 'new_username': new_username})


# ─────────────────────────────────────────────────────────────────────────────
# 6. API — Preview username (opsional, untuk auto-fill modal)
# ─────────────────────────────────────────────────────────────────────────────

@login_required
def api_preview_username(request, membro_id: int):
    membro = get_object_or_404(Membru, pk=membro_id)
    return JsonResponse({'username': _build_username(membro)})



@login_required
def my_profile(request):
    group = request.user.groups.all()[0].name
    user_mem = c_user_mem(request.user)
    
    if not user_mem:
        messages.warning(request, 'Profil la iha dadus membro.')
        return redirect('g-dash')
    
    obj = user_mem
    photo = Photo.objects.filter(membro=obj).first()
    contact = ContactInfo.objects.filter(membro=obj).first()
    location = LocationTL.objects.select_related(
        'municipality', 'administrativepost', 'village', 'aldeia'
    ).filter(membro=obj).first()
    position = MembroPosition.objects.select_related(
        'estructure', 'position'
    ).filter(membro=obj).first()
    formaleducations = FormalEducation.objects.filter(membro=obj, is_active=True)
    membrouser = MembroUser.objects.select_related('user').filter(membro=obj).first()

    context = {
        'title': f'Profil - {obj.name}',
        'legend': f'Profil - {obj.name}',
        'obj': obj,
        'photo': photo,
        'contact': contact,
        'location': location,
        'position': position,
        'formaleducations': formaleducations,
        'membrouser': membrouser,
        'group': group,
    }
    return render(request, 'users/profile.html', context)

@login_required
def AccountUpdate(request):
    group = request.user.groups.all()[0].name
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ita nia konta atualiza ona!')
            return redirect('user-account')
    else: form = UserForm(instance=request.user)
    context = {
        'group':group, 'form':form,
        'title':'Conta', 'legend':'Conta',
    }
    return render(request, 'auths/account.html', context)

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView

class UserPasswordChangeView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'auths/change_password.html'
    success_url = reverse_lazy('user-change-password-done')

class UserPasswordChangeDoneView(PasswordResetDoneView):
    template_name = 'auths/change_password_done.html'