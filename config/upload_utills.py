import os
from uuid import uuid4

def get_extension(filename):
    return filename.split('.')[-1]

def random_filename(field, ext):
    return f"{field}_{uuid4().hex}.{ext}"

def base_path(instance):
    return instance.__class__.__name__.lower()

def upload_estado(instance, filename):
    ext = get_extension(filename)
    model = base_path(instance)
    upload_to = f"{model}/estado/"
    name = random_filename("estado", ext)
    return os.path.join(upload_to, name)


def upload_photo(instance, filename):
    ext = get_extension(filename)
    model = base_path(instance)
    upload_to = f"{model}/photo/"
    name = random_filename("photo", ext)
    return os.path.join(upload_to, name)

def upload_formal(instance, filename):
    ext = get_extension(filename)
    model = base_path(instance)
    pk = instance.pk or uuid4().hex
    upload_to = f"{model}/formal/{pk}/"
    name = f"formal_{pk}.{ext}"
    return os.path.join(upload_to, name)


def upload_vote(instance, filename):
    ext = get_extension(filename)
    model = base_path(instance)
    pk = instance.pk or uuid4().hex
    upload_to = f"{model}/vote/{pk}/"
    name = f"vote_{pk}.{ext}"
    return os.path.join(upload_to, name)