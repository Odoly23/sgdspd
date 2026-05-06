from membro.models import Membru

def c_user_mem(user):
    objects = Membru.objects.filter(membrouser__user=user).prefetch_related('membrouser').first()
    obj = ""
    if objects: obj = objects
    return obj