import os
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class App(models.Model):

	key = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=48)
	description = models.CharField(max_length=144)
	illustration = models.URLField(max_length=500)
	trusted = models.BooleanField(default=False) # a trusted app does not need to be authorized by the user
	secret = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
	set_token_url = models.CharField(max_length=5000, help_text='eg: http://localhost:8008/auth/set-token/')
	callback_url = models.CharField(max_length=5000, help_text='eg: http://localhost:8008/auth/callback/')

	def __str__(self): return str(self.name)

	class Meta :
		verbose_name = 'application'
		verbose_name_plural = 'applications'


class NetworkUser(models.Model):

	user = models.OneToOneField(User, related_name='network_user') # see signals.py for NetworkUser creation
	uuid = models.UUIDField(max_length=32, default=uuid.uuid4)
	apps = models.ManyToManyField(App, through='Credentials')

	def number_of_apps(self):
		return self.apps.count()
	
	class Meta(object):
		verbose_name = _('membre du réseau')
		verbose_name_plural = _('membres du réseau')
		abstract = False
	
	def __str__(self):
		return str(self.user)



class Credentials(models.Model):
	''' Contains the token used to authenticate the user to the app '''
	app = models.ForeignKey(App, on_delete=models.CASCADE)
	network_user = models.ForeignKey(NetworkUser, on_delete=models.CASCADE)
	user_has_authorized = models.BooleanField(default=False)
	token = models.CharField(max_length=32, default=uuid.uuid4)
	date_joined = models.DateField(auto_now_add=True)

	def refresh_token(self):
		self.token = uuid.uuid4()
		self.save()

	class Meta(object):
		verbose_name = _('credential')
		verbose_name_plural = _('credentials')
