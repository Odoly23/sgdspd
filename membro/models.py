import datetime
import hashlib
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from custom.models import  BaseModel, Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram, \
						   Year, Estructure

from config.upload_utills import upload_photo, upload_estado, upload_formal
from django.core.exceptions import ValidationError
from datetime import date
import hashlib, uuid

class Membru(BaseModel):
    nu_id = models.CharField(max_length=15, verbose_name="Nu. Eleitoral", null=True, blank=False)
    name = models.CharField(max_length=200, null=True, verbose_name="Naran")
    pob = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fatin Moris")
    dob = models.DateField(null=True, verbose_name="Data Moris")
    sex = models.CharField(choices=[('Mane','Mane'),('Feto','Feto')], max_length=6, null=True, blank=True, verbose_name="Sexu")
    marital = models.CharField(choices=[('Solteiro/a','Solteiro/a'),('Casado/a','Casado/a'),('Divorciado/a','Divorciado/a'),('Viuvo/a','Viuvo/a')], max_length=15, null=True, blank=True, verbose_name="Estado Civil")
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Status")
    year = models.ForeignKey(Year, on_delete=models.CASCADE, null=True, verbose_name="Tinan", blank=True)
    file = models.FileField(upload_to=upload_estado, null=True, blank=True,
            validators=[FileExtensionValidator(allowed_extensions=['pdf'])], verbose_name="Anexa Eleitoral")
    datetime = models.DateTimeField(null=True, blank=True)
    hashed = models.CharField(max_length=128, null=True, blank=True)
    is_conf = models.BooleanField(default=False)
    date_conf = models.DateField(null=True, blank=True)
    conf_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="distconf")
    is_appr = models.BooleanField(default=False)
    date_appr = models.DateField(null=True, blank=True)
    appr_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='distappr')
    
    def __str__(self):
        return f'{self.name}'
        
    def age(self):
        if self.dob:
            today = date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return None
    def clean(self):
        super().clean()
        if self.dob:
            umur = self.age()
            if umur is not None and umur < 16:
                raise ValidationError({'dob': f'Idade tenke 16 anos ba leten. Idade agora: {umur} anos'})
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs) 
        if is_new and not self.hashed:
            self.hashed = hashlib.blake2b(f"{self.id}-{uuid.uuid4()}".encode()).hexdigest()
            super().save(update_fields=['hashed'])



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
	university = models.CharField(max_length=200, null=True, blank=True, verbose_name="Universidade/Entidade")
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

