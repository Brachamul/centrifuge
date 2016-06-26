from django.conf.urls import patterns, url

from . import views

urlpatterns = [
	url(r'^authorize/(?P<app_key>[\x00-\x7F]+)/(?P<user_uuid>[\x00-\x7F]+)/$', views.authorize, name='authorize'),
]