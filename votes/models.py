import datetime, uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from custom.models import BaseModel, Year, Position, Country, Municipality, AdministrativePost, Status, Village, SubVillage, EducationLevel, University, Faculty, StudyProgram
from membro.models import  Membru

class status_vote(BaseModel):
	is_close = models.BooleanField(default=True, null=True, blank=True)
	date_close = models.DateField(null=True, blank=True)
	data_lg = models.ForeignKey(Year, on_delete=models.CASCADE, null=True)
	is_open = models.BooleanField(default=False, null=True, blank=True)
	date_loke = models.DateField(null=True, blank=True)

	def __str__(self):
		return f"{self.date_close} - {self.data_lg}"

class VotingPlace(BaseModel):
    name = models.CharField(max_length=150, verbose_name="Naran Fatin Votu")
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, null=True)
    administrativepost = models.ForeignKey(AdministrativePost, on_delete=models.CASCADE, null=True)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
    aldeia = models.ForeignKey(SubVillage, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.village}"


class VotingResult(BaseModel):
    membro = models.ForeignKey(Membru, on_delete=models.CASCADE, related_name="voting_results")
    voting_place = models.ForeignKey(VotingPlace, on_delete=models.CASCADE, related_name="results")
    total_votes = models.IntegerField(default=0, verbose_name="Total Votu PD")
    photo = models.ImageField(upload_to='voting/', null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    note = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.voting_place} - {self.total_votes}"


class VotingAttachment(BaseModel):
    voting_result = models.ForeignKey(VotingResult, on_delete=models.CASCADE, related_name="attachments")
    image = models.ImageField(upload_to='voting/attachments/')