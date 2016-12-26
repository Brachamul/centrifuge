from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.site.site_header = 'Centrifuge - Administration'

urlpatterns = [
	url(r'^auth/', include('django.contrib.auth.urls')),
	url(r'^', include('auth_network_provider.urls')),
	url(r'^arriere-boutique/', admin.site.urls, name='admin'),
]