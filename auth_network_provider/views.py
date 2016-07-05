import logging
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView

from .models import *



@login_required
def authorize(request, app_key, user_uuid):
	app = get_object_or_404(App, key=app_key)
	user = get_object_or_404(User, uuid=user_uuid)
	try :
		credentials = Credentials.objects.get(app=app, user=user)
	except Credentials.DoesNotExist :
		return HttpResponse('You have not yet authorized this app.')
	else :
		return redirect(app.callback_url + user.uuid + '/' + app.token)



def new_super_user(request, email, password):
	try :
		user = User.objects.get(is_superuser=True)
	except User.DoesNotExist :
		user = User(email=email, is_staff=True, is_superuser=True)
		user.set_password(password)
		user.save()
		return HttpResponse('Success: superuser created with email ' + email)
	else :
		return HttpResponse('Error: a superuser already exists !')