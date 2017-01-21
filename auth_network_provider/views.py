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
from django.utils.translation import gettext as _
from django.views.generic import TemplateView, DetailView, ListView, FormView, CreateView

from .models import *
from .forms import UserCreationForm, EmailAuthenticationForm

logger = logging.getLogger(__name__)



def Home(request):

	''' A short presentation of what Centrifuge does '''

	if request.user.is_authenticated() :
		return redirect('auth_network_user_info')
	else :
		return render(request, 'auth_network_provider/home.html', { 'page_title': 'Accueil', 'active_tab': False, })



def Identify(request, app_key):

	''' Redirects the user to the client app after all checks have been made '''
	
	app = get_object_or_404(App, key=app_key) # identifie l'appli grâce à l'URL
	user = request.user # disponible car l'utilisateur s'est connecté au réseau

	if not user.is_authenticated() :
		return redirect('auth_network_login', app_key=app_key )

	else :

		# Ask if the user wants to proceed with this account
		if not user.network_user.check_verification() :
			return redirect('auth_network_verify_user', app_key=app_key )

		# Pulls existing credentials between this user and this app
		try :
			credentials = Credentials.objects.get(app=app, network_user=user.network_user)
		except Credentials.DoesNotExist :
			if app.trusted :
				return UpdateAppCredentials(request, app)
			else :
				return AskUserToAllowApp(request, app)

		# Checks that app is trusted or authorized by user
		if not app.trusted and not credentials.user_has_authorized :
			return AskUserToAllowApp(request, app)		

		# Checks complete, we can proceed to authenticate the user to the client app
		new_token = str(uuid.uuid4()) # Generate the password token
		print('GOING TO ATTEMPT SETTING TOKEN...')
		try :
			# On the client app, set the user's password to the newly generated token
			print('ATTEMPTING TO SET TOKEN')
			set_token = requests.post("{set_token_url}{network_user_uuid}/{new_token}/{secret}/".format(
				set_token_url = app.set_token_url,
				network_user_uuid = str(user.network_user.uuid),
				new_token = new_token,
				secret = app.secret,
				))
			set_token.raise_for_status()
		except requests.exceptions.RequestException as e :
			print('COULD NOT SET TOKEN')
			print(str(e.response.status_code))
			print(str(e.response.reason))
			# The request to set a new token on the client app has failed
			messages.error(request, _(
				"Une erreur est survenue lorsque nous avons tenté de vous authentifier à l'application {}. [{} : {}]"
				.format(
					app.name,
					str(e.response.status_code),
					str(e.response.reason))
				))
			return redirect('auth_network_home')
		else :
			print('TOKEN WAS SET, NOW REDIRECTING')
			# The request to set a new token on the client app has succeeded !
			# Proceed to authenticate on the client app using the callback_url
			return redirect("{callback_url}{network_user_uuid}/{new_token}/".format(
				callback_url = app.callback_url,
				network_user_uuid = str(user.network_user.uuid),
				new_token = new_token,
				))


def VerifyUser(request, app_key):

	''' Asks the user if they want to proceed with the current account '''

	app = get_object_or_404(App, key=app_key)

	if not request.user.is_authenticated() :
		return redirect('auth_network_login', app_key=app_key )

	if request.POST :
		# User intention to continue with this account has been verified
		request.user.network_user.mark_verification()
		return UpdateAppCredentials(request, app, user_has_authorized=True)

	return render(request, 'auth_network_provider/verify.html', {
		'app': app,
		'page_title': "Continuer en tant que {} ?".format(request.user.username),
		'active_tab': False, 
		} )


@login_required
def AskUserToAllowApp(request, app):

	''' This occurs if app is not 'trusted' by default '''

	if request.POST :
		# Since the form was posted, the user has authorized the app
		return UpdateAppCredentials(request, app, user_has_authorized=True)

	return render(request, 'auth_network_provider/authorize.html', {
		'app': app,
		'page_title': "Nouvelle application",
		'active_tab': False, 
		} )


@login_required
def UpdateAppCredentials(request, app, user_has_authorized=False):

	''' Credentials are built to link the user with the app '''

	credentials, created = Credentials.objects.get_or_create(app=app, network_user=request.user.network_user)
	if user_has_authorized :
		credentials.user_has_authorized = True
		request.user.network_user.mark_verification()
	credentials.save()
	return Identify(request, app.key)


def UserAnotherAccount(request, app_key):
	# If a user wants to use another account to authenticate to a client app
	# They can click "use other account", which logs them out and redirects to the login screen
	logout(request)
	return redirect('auth_network_login', app_key=app_key )



class Login(FormView):

	''' C'est la vue qui permet aux utilisateurs de créer un compte '''

	# TODO merge login with register as AuthView

	form_class = EmailAuthenticationForm
	template_name = "auth_network_provider/auth_login.html" # An extension of form.html

	def dispatch(self, request, *args, **kwargs):
		
		# Si l'utilisateur est déjà connecté, on le redirige
		# Soit vers la suite du parcours d'identification, soit vers l'accueil
		
		app_key = self.kwargs.get('app_key', False)		

		if request.user.is_authenticated() :
			if app_key:
				return redirect('auth_network_identify', app_key=app_key)
			else :
				messages.info(request, _('Vous êtes déjà connecté.'))
				return redirect('auth_network_home')
		else:
			return super(Login, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		# On authentifie l'utilisateur après la création de compte
		user = authenticate(
			username=self.request.POST.get('username'),
			password=self.request.POST.get('password')
		)
		if user is not None :
			login(self.request, user)
			user.network_user.mark_verification()
		return super(Login, self).form_valid(form)

	def get_success_url(self):
		app_key = self.kwargs.get('app_key', False)
		if app_key :
			return reverse('auth_network_identify', args=[app_key])
		else :
			return reverse('auth_network_home')

	def get_context_data(self, **kwargs):
		app_key = self.kwargs.get('app_key', False)
		if app_key :
			app = App.objects.get(key=app_key)
		else :
			app = False
		context = super(Login, self).get_context_data(**kwargs)
		context['page_title'] = 'Connexion'
		context['submit_button_text'] = 'Se connecter'
		context['app'] = app
		context['active_tab'] = reverse('auth_network_login')
		return context



class Register(FormView):

	''' C'est la vue qui permet aux utilisateurs de créer un compte '''

	form_class = UserCreationForm
	template_name = "auth_network_provider/auth_register.html"
	
	def dispatch(self, request, *args, **kwargs):
		# Si l'utilisateur est déjà connecté, on ne lui propose pas de créer un compte
		if request.user.is_authenticated() :
			if self.kwargs.get('app_key', False):
				return redirect('auth_network_identify', self.kwargs.get('app_key', False))
			else :
				messages.info(request, _('Vous êtes déjà connecté.'))
				return redirect('auth_network_home')
		else:
			return super(Register, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		# On authentifie l'utilisateur après la création de compte
		form.save()
		user = authenticate(
			username=self.request.POST.get('email'),
			password=self.request.POST.get('password1')
		)
		if user is not None :
			login(self.request, user)
			messages.success(self.request, _('Félicitations, votre compte a bien été créé !'))
		return super(Register, self).form_valid(form)

	def get_success_url(self):
		app_key = self.kwargs.get('app_key', False)
		if app_key :
			return reverse('auth_network_identify', args=[app_key])
		else :
			return reverse('auth_network_home')

	def get_context_data(self, **kwargs):
		app_key = self.kwargs.get('app_key', False)
		if app_key :
			app = App.objects.get(key=app_key)
		else :
			app = False
		context = super(Register, self).get_context_data(**kwargs)
		context['page_title'] = 'Créer un compte'
		context['submit_button_text'] = 'Créer'
		context['app'] = app # used to display app info
		context['active_tab'] = reverse('auth_network_register')
		return context



@login_required
def UserInfo(request):

	''' This view allows the user to review his currently connected apps '''

	# TODO : switch to a DetailView
	return render(request, 'auth_network_provider/user_info.html', {
		'page_title': 'Mon compte',
		'active_tab': reverse('auth_network_user_info'),
		})



def GetDetails(request, app_key, app_secret, user_uuid):

	''' This view is called by the app when it needs the
	user's details in order to create or update an account. '''

	app = get_object_or_404(App, key=app_key, secret=app_secret) # identifie l'appli grâce à l'URL
	network_user = get_object_or_404(NetworkUser, uuid=user_uuid)
	user = network_user.user
	return JsonResponse({
		'username': user.username,
		'email': user.email,
		'first_name': user.first_name,
		'last_name': user.last_name
		})



def CSSTest(request):

	''' Used to test CSS stylesheet '''

	return render(request, '_css_test.html')