import logging
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView

from .models import *



@login_required
def Identify(request, app_key):
	''' Now that the user is logged in, let's find out what app he's asking access to '''
	app = get_object_or_404(App, key=app_key) # identifie l'appli grâce à l'URL
	user = request.user # disponible car l'utilisateur s'est connecté au réseau
	try :
		credentials = Credentials.objects.get(app=app, user=user)
	except Credentials.DoesNotExist :
		if app.trusted :
			return AddAppToUserProfile(request, app, user)
		else :
			return AskUserToAllowApp(request, app, user)
	else :
		return BackToClientApp(request, app=app, user=user)


def AskUserToAllowApp(request, app, user):
	''' This occurs if app is not 'trusted' by default '''
	# TODO : build this feature :p
	return HttpResponse("Cette appli n'est pas encore validée.")
#	return AddAppToUserProfile(request, app, user)
#	return render(request, 'auth_network_provider/allow.html', {'page_title': "Autoriser une application"})


def AddAppToUserProfile(request, app, user):
	''' Credentials are built to link the user with the app '''
	new_credentials = Credentials(user=user, app=app)
	new_credentials.save()
	return BackToClientApp(request, app=app, user=user)


def BackToClientApp(request, app, user):
	''' We've done all we need and can go back to the client app
		Let's set the token on the client app with a POST request
		So that the client app can recognize our browser request '''
	token = str(uuid.uuid4())
	setTokenUrl = app.set_token_url + '/' + str(user.uuid) + '/' + token + '/' + app.secret + '/'
	requests.get(app.set_token_url + '/' + str(user.uuid) + '/' + token + '/' + app.secret + '/')
	# TODO : change the previous request to a "POST"
	return redirect(app.callback_url + '/' + str(user.uuid) + '/' + token)



def GetDetails(request, app_key, app_secret, user_uuid):
	''' An app wants to create an account for a user and needs their details '''
	app = get_object_or_404(App, key=app_key, secret=app_secret) # identifie l'appli grâce à l'URL
	user = get_object_or_404(User, uuid=user_uuid)
	return JsonResponse({'username': user.name, 'email': user.email})



# Only when first installing the network
def NewSuperUser(request, email, password):
	try :
		user = User.objects.get(is_superuser=True)
	except User.DoesNotExist :
		user = User(email=email, is_staff=True, is_superuser=True)
		user.set_password(password)
		user.save()
		return HttpResponse('Success: superuser created with email ' + email)
	else :
		return HttpResponse('Error: a superuser already exists !')