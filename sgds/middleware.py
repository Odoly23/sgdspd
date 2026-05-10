
# middleware.py
import hashlib
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response

class PreviousURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['previous_url'] = request.META.get('HTTP_REFERER', None)
        response = self.get_response(request)
        return response

class NoBackAfterLogout(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if request.path in [reverse('login')]:
                return redirect('/')
        return None

    def process_response(self, request, response):
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


# ✅ TAMBAHKAN MIDDLEWARE BARU INI
class PreventDuplicatePostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            
            # Handle file upload (foto, pdf, dll)
            file_info = ''
            if request.FILES:
                file_info = str(sorted([
                    (k, v.name, v.size)
                    for k, v in request.FILES.items()
                ]))

            post_data_str = request.path + str(sorted(request.POST.items())) + file_info
            post_hash = hashlib.md5(post_data_str.encode()).hexdigest()

            last_hash = request.session.get('last_post_hash')
            last_path = request.session.get('last_post_path')

            if last_hash == post_hash and last_path == request.path:
                previous_url = request.session.get('previous_url') or '/'
                messages.warning(request, 'Dadus rejistadu ona. La bele submete fila fali.')
                return redirect(previous_url)

            request.session['last_post_hash'] = post_hash
            request.session['last_post_path'] = request.path

        response = self.get_response(request)

        if request.method == 'POST' and response.status_code == 302:
            request.session.pop('last_post_hash', None)
            request.session.pop('last_post_path', None)

        return response