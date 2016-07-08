from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^identify/(?P<app_key>[\x00-\x7F]+)/$', views.Identify, name='network_auth_identify'),
	url(r'^get-details/(?P<app_key>[\x00-\x7F]+)/(?P<app_secret>[\x00-\x7F]+)/(?P<user_uuid>[\x00-\x7F]+)/$', views.GetDetails, name='network_auth_get_details'),
	url(r'^new-super-user/(?P<email>[\x00-\x7F]+)/(?P<password>[\x00-\x7F]+)/$', views.NewSuperUser, name='network_auth_new_super_user'),
]