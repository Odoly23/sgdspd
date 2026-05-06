import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class BaseModel(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_updated")
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="%(class)s_deleted")
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = models.Manager()
    active_objects = ActiveManager()

    def soft_delete(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save()

    def restore(self):
        self.deleted_at = None
        self.deleted_by = None
        self.save()

    class Meta:
        abstract = True

class Estructure(BaseModel):
	code = models.CharField(max_length=5, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Position(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class EducationLevel(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Country(BaseModel):
	code = models.CharField(max_length=5)
	name = models.CharField(max_length=50, verbose_name="Naran")

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Municipality(BaseModel):
	code = models.CharField(max_length=5, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	hckey = models.CharField(max_length=10, null=True)

	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class AdministrativePost(BaseModel):
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Village(BaseModel):
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class SubVillage(BaseModel):
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class University(BaseModel):
	country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Faculty(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class StudyProgram(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Area(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Naran")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)
class Year(BaseModel):
	year = models.IntegerField(null=True, blank=True)
	is_active = models.BooleanField(default=False)
	def __str__(self):
		template = '{0.year}'
		return template.format(self)

class Language(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Lingua")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)

class Status(BaseModel):
	name = models.CharField(max_length=100, verbose_name="Status")
	def __str__(self):
		template = '{0.name}'
		return template.format(self)


