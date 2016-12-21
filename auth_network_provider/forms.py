from registration.forms import RegistrationForm

from .models import User

class CustomUserRegistrationForm(RegistrationForm):
    class Meta:
        model = User
        fields = ['name', 'email', ]