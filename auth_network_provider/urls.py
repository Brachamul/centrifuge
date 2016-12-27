from django.conf.urls import url, include

from . import views

APP_KEY = r'(?P<app_key>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' # UUID
APP_SECRET = r'(?P<app_secret>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' # UUID
USER_UUID = r'(?P<user_uuid>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})' # UUID

urlpatterns = [
	url(r'^$', views.Home, name='auth_network_home'),
	url(r'^identify/{}/'.format(APP_KEY), views.Identify, name='auth_network_identify'),
	url(r'^login/', include([
		url(r'^$', views.Login.as_view(), name='auth_network_login'),
		url(r'{}/'.format(APP_KEY), views.Login.as_view(), name='auth_network_login'),
	])),
	url(r'^register/', include([
		url(r'^$', views.Register.as_view(), name='auth_network_register'),
		url(r'{}/'.format(APP_KEY), views.Register.as_view(), name='auth_network_register'),
	])),
	url(r'^verify/{}/'.format(APP_KEY), views.VerifyUser, name='auth_network_verify_user'),
	url(r'^use-another-account/{}/'.format(APP_KEY), views.UserAnotherAccount, name='auth_network_use_another_account'),
	url(r'^account/$', views.UserInfo, name='auth_network_user_info'),
	url(r'^get-details/{APP_KEY}/{APP_SECRET}/{USER_UUID}/$'.format(
		APP_KEY = APP_KEY,
		APP_SECRET = APP_SECRET,
		USER_UUID = USER_UUID,
		), views.GetDetails, name='auth_network_get_details'
	),
]

