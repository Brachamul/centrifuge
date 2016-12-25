from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.utils.translation import gettext as _

from .models import User



class UserCreationForm(forms.ModelForm):
	"""
	A form that creates a user, with no privileges, from the given username, email and
	password. This is a slight modification of the default UserCreateForm to follow the
	custom user model with email as login and fewer username restrictions.
	"""
	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
	}
	password1 = forms.CharField(label=_("Password"),
		strip=False,
		widget=forms.PasswordInput)
	password2 = forms.CharField(label=_("Password confirmation"),
		widget=forms.PasswordInput,
		strip=False,
		help_text=_("Enter the same password as before, for verification."))

	class Meta:
		model = User
		fields = ("username", "email")

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

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user