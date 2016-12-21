import os
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import gettext as _


class App(models.Model):
	key = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	trusted = models.BooleanField(default=False) # a trusted app does not need to be authorized by the user
	secret = models.CharField(max_length=32, default=uuid.uuid4, editable=False)
	set_token_url = models.CharField(max_length=5000, help_text='eg: http://localhost:8008/auth/set-token/')
	callback_url = models.CharField(max_length=5000, help_text='eg: http://localhost:8008/auth/callback/')
	def __str__(self): return str(self.name)
	class Meta :
		verbose_name = 'application'
		verbose_name_plural = 'applications'


# http://stackoverflow.com/questions/35528074/django-is-extending-abstractbaseuser-required-to-use-email-as-username-field

class User(AbstractBaseUser, PermissionsMixin):

	uuid = models.UUIDField(max_length=32, default=uuid.uuid4)
	
	apps = models.ManyToManyField(App, through='Credentials')

	username = models.CharField(max_length=32, blank=True, null=True)
	# TODO : this is useless because we're using the email as logging, but the createsuperuser() function
	# doesn't work without it... here is the error message :
	# TypeError: create_superuser() missing 1 required positional argument: 'username'
	
	email = models.EmailField(
		_('Email'), unique=True,
		error_messages={
			'unique': _("A user with that email already exists."),
		}
	)
	name = models.CharField(
		_('Prénom et Nom'), max_length=255,
	)
	is_staff = models.BooleanField(
		_('Staff Status'), default=False,
		help_text=_('Designates whether the user can log into this admin '
					'site.')
	)
	is_active = models.BooleanField(
		_('Active'), default=True,
		help_text=_('Designates whether this user should be treated as '
					'active. Unselect this instead of deleting accounts.')
	)
	
	date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
	
	objects = UserManager()
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'username']

	def number_of_apps(self):
		return self.apps.count()
	
	class Meta(object):
		verbose_name = _('user')
		verbose_name_plural = _('users')
		abstract = False
	
	def get_full_name(self):
		return self.name
	
	def get_short_name(self):
		return self.name
	
	def __str__(self):
		return str(self.name)
	
	def email_user(self, subject, message, from_email=None, **kwargs):
		""" Sends an email to this User. """
		send_mail(subject, message, from_email, [self.email], **kwargs)



class Credentials(models.Model):
	''' Contains the token used to authenticate the user to the app '''
	app = models.ForeignKey(App, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	user_has_authorized = models.BooleanField(default=False)
	token = models.CharField(max_length=32, default=uuid.uuid4)
	date_joined = models.DateField(auto_now_add=True)

	def refresh_token(self):
		self.token = uuid.uuid4()
		self.save()

	class Meta(object):
		verbose_name = _('credential')
		verbose_name_plural = _('credentials')

