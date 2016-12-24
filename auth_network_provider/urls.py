from django.conf.urls import url, include

from . import views

# This is for Django-Registration
from registration.backends.simple.views import RegistrationView
from .forms import CustomUserRegistrationForm

urlpatterns = [
	url(r'^$', views.Home, name='network_auth_home'),
	url(r'^identify/(?P<app_key>[\x00-\x7F]+)/$', views.Identify, name='network_auth_identify'),
	url(r'^register/', include([
		url(r'^$', RegistrationView.as_view(form_class=CustomUserRegistrationForm), name='registration_register'),
		url(r'^(?P<app_key>[\x00-\x7F]+)/$', views.Register.as_view(), name='network_auth_register_for_app'),
	])),
	url(r'^get-details/(?P<app_key>[\x00-\x7F]+)/(?P<app_secret>[\x00-\x7F]+)/(?P<user_uuid>[\x00-\x7F]+)/$', views.GetDetails, name='network_auth_get_details'),
	url(r'^new-super-user/(?P<email>[\x00-\x7F]+)/(?P<password>[\x00-\x7F]+)/$', views.NewSuperUser, name='network_auth_new_super_user'),
]