import datetime
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from custom.models import  BaseModel, Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram, \
						   Year, Estructure

from config.upload_utills import upload_photo, upload_estado, upload_formal

class Membru(BaseModel):
	nu_id = models.CharField(max_length=15, verbose_name="Nu. Eleitoral", null=True, blank=False)
	name= models.CharField(max_length=200, null=True, verbose_name="Naran")
	pob = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fatin Moris")
	dob = models.DateField(null=True, verbose_name="Data Moris")
	sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=6, null=True, blank=True, verbose_name="Sexu")
	marital = models.CharField(choices=[('Solteiro/a','Solteiro/a'),('Casado/a','Casado/a'),('Divorciado/a','Divorciado/a'),('Viuvo/a','Viuvo/a')], max_length=15, null=True, blank=True, verbose_name="Estado Civil")
	status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, verbose_name="Status")
	year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, verbose_name="Tinan", blank=True)
	file = models.FileField(upload_to=upload_estado, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anexa Eleitoral")
	datetime = models.DateTimeField(null=True)
	hashed = models.CharField(max_length=128, null=True)

	
	def __str__(self):
		template = '{0.name}'
		return template.format(self)
	def age(self):
		if self.dob:
			return int((datetime.date.today() - self.dob).days / 365.25)
		return None

	def save(self, *args, **kwargs):
		if not self.hashed:
			temp_id = self.id or 0
			self.hashed = hashlib.blake2b(str(temp_id).encode()).hexdigest()
		super().save(*args, **kwargs)

class ContactInfo(BaseModel):
	membro = models.OneToOneField(Membru, on_delete=models.CASCADE, related_name='contactinfo')
	email = models.CharField(max_length=50, null=True, blank=True)
	phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Nu. Telemovel")
	datetime = models.DateTimeField(null=True)
	hashed = models.CharField(max_length=128, null=True)

	def __str__(self):
		template = '{0.membro} {0.email} {0.phone}'
		return template.format(self)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if not self.hashed:
			self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
			super().save(update_fields=['hashed'])


class LocationTL(BaseModel):
	membro = models.OneToOneField(Membru, on_delete=models.CASCADE, related_name='locationtl')
	municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Municipiu")
	administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Posto")
	village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Suco")
	aldeia = models.ForeignKey(SubVillage, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Aldeia")
	datetime = models.DateTimeField(null=True)
	hashed = models.CharField(max_length=128, null=True)

	def __str__(self):
		template = '{0.membro} {0.municipality}'
		return template.format(self)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if not self.hashed:
			self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
			super().save(update_fields=['hashed'])


class AddressOrigin(BaseModel):
	membro = models.OneToOneField(Membru, on_delete=models.CASCADE, related_name='addressorigin')
	city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Cidade")
	address = models.CharField(max_length=50, null=True, blank=True, verbose_name="Enderesu")
	datetime = models.DateTimeField(null=True)
	
	def __str__(self):
		template = '{0.membro} {0.city}'
		return template.format(self)

class Photo(BaseModel):
	membro = models.OneToOneField(Membru, on_delete=models.CASCADE, related_name='photo')
	image = models.ImageField(default='default.png', upload_to=upload_photo, null=True)
	datetime = models.DateTimeField(null=True)
	
	def __str__(self):
		template = '{0.membro}'
		return template.format(self)

class FormalEducation(BaseModel):
	membro = models.ForeignKey(Membru, on_delete=models.CASCADE, related_name="formaleducation")
	educationlevel = models.ForeignKey(EducationLevel, on_delete=models.CASCADE, related_name="formaleducation", verbose_name="Nivel Edukasaun")
	university = models.ForeignKey(University, null=True, blank=True, on_delete=models.CASCADE, related_name="formaleducation", verbose_name="Universidade/Entidade")
	faculty = models.CharField(max_length=100, null=True, blank=True, verbose_name="Faculdade")
	studyprogram = models.CharField(max_length=100, null=True, blank=True, verbose_name="Programa Estudu/Curso")
	area =  models.CharField(max_length=200, null=True, blank=True, verbose_name="Area Professional")
	graduation_year = models.DateField(null=True, blank=True, verbose_name="Data Gradua")
	summary = models.TextField(null=True, blank=True, verbose_name="Sumariu")
	file = models.FileField(upload_to=upload_formal, null=True, blank=True,
			validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anexu Certificado")
	is_active = models.BooleanField(default=True)
	datetime = models.DateTimeField(null=True)
	hashed = models.CharField(max_length=128, null=True)
	
	def __str__(self):
		template = '{0.membro} {0.educationlevel}'
		return template.format(self)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if not self.hashed:
			self.hashed = hashlib.blake2b(str(self.id).encode()).hexdigest()
			super().save(update_fields=['hashed'])


class MembroUser(BaseModel):
    membro = models.OneToOneField(Membru, on_delete=models.CASCADE, null=True, blank=True, related_name="membrouser")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)




class MembroPosition(BaseModel):
	membro = models.OneToOneField(Membru, on_delete=models.CASCADE, related_name="membroposition", verbose_name="Pessoal")
	estructure = models.ForeignKey(Estructure, on_delete=models.CASCADE, null=True, verbose_name="Estrutura")
	position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True, related_name="membroposition", verbose_name="Pojisaun")
	datetime = models.DateTimeField(null=True)
	
	def __str__(self):
		template = '{0.position}'
		return template.format(self)

