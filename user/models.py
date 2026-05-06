from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class AuditLogin(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="audituserlogin")
	login_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

		
	def __str__(self):
		template = '{0.user}, {0.login_time}'
		return template.format(self)
