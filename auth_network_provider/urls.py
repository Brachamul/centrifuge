from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^authorize/(?P<app_key>[\x00-\x7F]+)/(?P<user_uuid>[\x00-\x7F]+)/$', views.authorize, name='authorize'),
	url(r'^new_super_user/(?P<email>[\x00-\x7F]+)/(?P<password>[\x00-\x7F]+)/$', views.new_super_user, name='new_super_user'),
]