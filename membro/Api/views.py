# membro/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from membro.models import Membru, MembroUser
from django.urls import reverse

class APINotifBadgeMembro(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        groups = list(user.groups.values_list('name', flat=True))
        count = 0

        if 'suku' in groups:
            try:
                village = user.membrouser.membro.locationtl.village
                count = Membru.objects.filter(
                    locationtl__village=village,
                    is_conf=False
                ).count()
            except Exception:
                count = 0

        elif 'postu' in groups:
            count = Membru.objects.filter(
                is_conf=True,
                is_appr=False
            ).count()

        return Response({'value': count})


class APINotifPediduFounMembro(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        groups = list(user.groups.values_list('name', flat=True))
        result = []

        if 'suku' in groups:
            try:
                village = user.membrouser.membro.locationtl.village
                count = Membru.objects.filter(
                    locationtl__village=village,
                    is_conf=False
                ).count()
                result.append({
                    'label': 'Membro Seidauk Konfirma',
                    'count': count,
                    'url': reverse('list-pending-conf')
                })
            except Exception:
                pass

        elif 'postu' in groups:
            count = Membru.objects.filter(
                is_conf=True,
                is_appr=False
            ).count()
            result.append({
                'label': 'Membro Seidauk Aprova',
                'count': count,
                'url': reverse('list-pending-appr')
            })

        return Response({'items': result})