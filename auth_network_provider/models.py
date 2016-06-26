import os
import uuid
from django.db import models
from django.conf import settings

from django.contrib.auth.models import User



class NetworkApp(models.Model):
	name = models.CharField(max_length=255)
	uuid = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
	secret = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
	new_token_url = models.CharField(max_length=5000)
	callback_url = models.CharField(max_length=5000)



class NetworkUser(models.Model):
	user = models.OneToOneField(User)
	uuid = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
	apps = models.ManyToManyField(NetworkApp, through=Credentials)



class Credentials(models.Model):
	app = models.ForeignKey(NetworkApp, on_delete=models.CASCADE, editable=False)
	user = models.ForeignKey(NetworkUser, on_delete=models.CASCADE, editable=False)
	token = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
	date_joined = models.DateField(auto_now_add=True, editable=False)

	def refresh_token(self):
		self.token = uuid.uuid4()
		self.save()