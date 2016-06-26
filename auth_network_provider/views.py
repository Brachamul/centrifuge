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
def authorize(request, app_key):
	get_object_or_404(NetworkApp, uuid=user_uuid)
	# TODO : set a new token at this point
	post_data = {'app_secret': network_app.secret, 'user_uuid': network_user.uuid, 'token': network_user.token}
	response = requests.post(network_app.new_token_url, data=post_data)
	print()
	print()
	print(response.content)
	print()
	print()
	return redirect(network_app.callback_url + network_user.uuid + '/' + network_user.token)