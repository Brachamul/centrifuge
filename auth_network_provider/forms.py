from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _

from .models import User



class UserCreationForm(forms.ModelForm):
	"""
	A form that creates a user, with no privileges, from the given first name, last name, email and
	password. This is a modification of the default UserCreateForm to follow the custom user model
	with email as login and get_full_name() as username.
	"""
	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
		'email_already_taken': _("Cette adresse électronique est déjà enregistrée."),
	}

	password1 = forms.CharField(
		label=_("Password"),
		strip=False,
		widget=forms.PasswordInput(),
		)

	password2 = forms.CharField(
		label=_("Password confirmation"),
		strip=False,
		widget=forms.PasswordInput(),
		help_text=_("Enter the same password as before, for verification.")
		)

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', )
		required_fields = fields

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError(
				self.error_messages['password_mismatch'],
				code='password_mismatch',
			)
		self.instance.username = self.cleaned_data.get('username')
		password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
		return password2

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if User.objects.filter(email=email).count() > 0 :
			raise forms.ValidationError(
				self.error_messages['email_already_taken'],
				code='email_already_taken',
			)
		password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
		return email


	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.username = user.get_full_name()

		# L'username est généré à partir du prénom + nom
		# Si un homonyme existe dans la base, on fait "Barnaby Brachamul #2"
		homonyms = User.objects.filter(username=user.username)
		if homonyms :
			user.username = '{name} #{number}'.format(
				name=user.username,
				number=(homonyms.count() + 1)
			)
		if commit:
			user.save()
		return user



class EmailAuthenticationForm(AuthenticationForm):

	def __init__(self, *args, **kwargs):
		super(EmailAuthenticationForm, self).__init__(*args, **kwargs)
		self.fields['username'] = forms.EmailField(
			label=_("Email"),
			max_length=254,
			)