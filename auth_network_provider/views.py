import logging
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView

from .models import *
from .forms import UserCreationForm

logger = logging.getLogger(__name__)


def Home(request): return render(request, 'auth_network_provider/home.html', { 'page_title': 'Accueil' })



@login_required
def Identify(request, app_key):
	''' Now that the user is logged in, let's find out what app he's asking access to '''
	app = get_object_or_404(App, key=app_key) # identifie l'appli grâce à l'URL
	user = request.user # disponible car l'utilisateur s'est connecté au réseau
	try :
		credentials = Credentials.objects.get(app=app, user=user)
	except Credentials.DoesNotExist :
		if app.trusted :
			return AddAppToUserProfile(request, app)
		else :
			return AskUserToAllowApp(request, app)
	else :
		if app.trusted or credentials.user_has_authorized :
			return BackToClientApp(request, app)
		else :
			return AskUserToAllowApp(request, app)


@login_required
def AskUserToAllowApp(request, app):
	''' This occurs if app is not 'trusted' by default '''
	return render(request, 'auth_network_provider/authorize.html', {
		'app': app,
		'page_title': "Autoriser une application",
		} )
#	return AddAppToUserProfile(request, app, user)
#	return render(request, 'auth_network_provider/allow.html', {'page_title': "Autoriser une application"})


@login_required
def AddAppToUserProfile(request, app):
	''' Credentials are built to link the user with the app '''
	new_credentials = Credentials(app=app, user=request.user)
	new_credentials.save()
	return BackToClientApp(request, app=app, user=request.user)


@login_required
def BackToClientApp(request, app):
	''' We've done all we need and can go back to the client app
		Let's set the token on the client app with a POST request
		So that the client app can recognize our browser request '''
	token = str(uuid.uuid4())
	requests.post(app.set_token_url + str(request.user.uuid) + '/' + token + '/' + app.secret + '/')
	return redirect(app.callback_url + str(request.user.uuid) + '/' + token + '/')


# Secret instead of login_required
def GetDetails(request, app_key, app_secret, user_uuid):
	''' An app wants to create an account for a user and needs their details '''
	app = get_object_or_404(App, key=app_key, secret=app_secret) # identifie l'appli grâce à l'URL
	user = get_object_or_404(User, uuid=user_uuid)
	return JsonResponse({'username': user.name, 'email': user.email})



class Register(FormView):

	''' C'est la vue qui permet aux utilisateurs de créer un compte '''
	form_class = UserCreationForm
	template_name = "form.html"
	success_url = "/"

	def get_context_data(self, **kwargs):
		context = super(Register, self).get_context_data(**kwargs)
		context['page_title'] = 'Créer un compte'
		context['submit_button_text'] = 'Créer'
		return context

	def form_valid(self, form):
		form.save()
		messages.success(self.request, 'Félicitations, {}, votre compte a bien été créé !'.format(self.request.POST.get('username')))
		user = authenticate(email=self.request.POST.get('email'), password=self.request.POST.get('password1'))
		print('USER :' + user)
		if user is not None :
			login(self.request, user)
		return super(Register, self).form_valid(form)


class RegisterForApp(Register):

	def get_success_url(self):

		''' Si la création de compte intervient alors que l'utilisateur
		souhaitait se connecter à l'une des applications de la base,
		on le redirige vers le parcours d'identification correspondant. '''
		if 'app_key' in self.kwargs :
			return redirect('network_auth_identify', app_key=self.kwargs['app_key'])
		else :
			return redirect('/')