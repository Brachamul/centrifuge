from django.conf.urls import url, include

from . import views

APP_KEY = r'(?P<app_key>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' # UUID
APP_SECRET = r'(?P<app_secret>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' # UUID
USER_UUID = r'(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' # UUID

urlpatterns = [
	url(r'^$', views.Home, name='network_auth_home'),
	url(r'^identify/{}/$'.format(APP_KEY), views.Identify, name='network_auth_identify'),
	url(r'^register/', include([
		url(r'^$', views.Register.as_view(), name='registration_register'),
		url(r'^{}/$'.format(APP_KEY), views.RegisterForApp.as_view(), name='network_auth_register_for_app'),
	])),
	url(r'^get-details/{APP_KEY}/{APP_SECRET}/{USER_UUID}/$'.format(
		APP_KEY = APP_KEY,
		APP_SECRET = APP_SECRET,
		USER_UUID = USER_UUID,
		), views.GetDetails, name='network_auth_get_details'),
]