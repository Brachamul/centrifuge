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
	if request.user.is_authenticated() :
		return redirect('auth_network_user_info')
	else :
		return render(request, 'auth_network_provider/home.html', { 'page_title': 'Accueil' })



def Identify(request, app_key):
	''' Now that the user is logged in, let's find out what app he's asking access to '''
	
	app = get_object_or_404(App, key=app_key) # identifie l'appli grâce à l'URL
	user = request.user # disponible car l'utilisateur s'est connecté au réseau

	if not user.is_authenticated() :
		return redirect('auth_network_login', app_key=app.key )
	else :
		try :
			credentials = Credentials.objects.get(app=app, network_user=user.network_user)
		except Credentials.DoesNotExist :
			if app.trusted :
				return UpdateAppCredentials(request, app)
			else :
				return AskUserToAllowApp(request, app)
		else :
			if not app.trusted and not credentials.user_has_authorized :
				return AskUserToAllowApp(request, app)		
			else :
				# The app is authorized or trusted by an authenticated user
				# We can proceed to authenticate them to the client app
				new_token = str(uuid.uuid4()) # Generate the password token
				try :
					# On the client app, set the user's password to the newly generated token
					requests.post("{set_token_url}{network_user_uuid}/{new_token}/{secret}/".format(
						set_token_url = app.set_token_url,
						network_user_uuid = str(user.network_user.uuid),
						new_token = new_token,
						secret = app.secret,
						))
				except requests.exceptions.RequestException :
					# The request to set a new token on the client app has failed
					messages.error(_(
						"Une erreur est survenue lorsque nous avons tenté de contacter l'application {}."
						.format(app.name)))
					return redirect('auth_network_home')
				else :
					# The request to set a new token on the client app has succeeded !
					# Proceed to authenticate on the client app using the callback_url
					return redirect("{callback_url}{network_user_uuid}/{new_token}/".format(
						callback_url = app.callback_url,
						network_user_uuid = str(user.network_user.uuid),
						new_token = new_token,
						))


@login_required
def AskUserToAllowApp(request, app):
	''' This occurs if app is not 'trusted' by default '''
	if request.POST :
		# Since the form was posted, the user has authorized the app
		return UpdateAppCredentials(request, app, user_has_authorized=True)
	return render(request, 'auth_network_provider/authorize.html', {
		'app': app,
		'page_title': "Nouvelle application",
		} )

@login_required
def UpdateAppCredentials(request, app, user_has_authorized=False):
	''' Credentials are built to link the user with the app '''
	credentials, created = Credentials.objects.get_or_create(app=app, network_user=request.user.network_user)
	if user_has_authorized : credentials.user_has_authorized = True
	credentials.save()
	return Identify(request, app.key)

# Secret instead of login_required
def GetDetails(request, app_key, app_secret, user_uuid):
	''' An app wants to create an account for a user and needs their details '''
	app = get_object_or_404(App, key=app_key, secret=app_secret) # identifie l'appli grâce à l'URL
	network_user = get_object_or_404(NetworkUser, uuid=user_uuid)
	user = network_user.user
	return JsonResponse({
		'username': user.username,
		'email': user.email,
		'first_name': user.first_name,
		'last_name': user.last_name
		})



class Login(FormView):

	''' C'est la vue qui permet aux utilisateurs de créer un compte '''

	form_class = EmailAuthenticationForm
	template_name = "login.html" # An extension of form.html

	def dispatch(self, request, *args, **kwargs):
		# Si l'utilisateur est déjà connecté, on le redirige
		# Soit vers la suite du parcours d'identification, soit vers l'accueil
		if request.user.is_authenticated() :
			if self.kwargs.get('app_key', False):
				return redirect('auth_network_identify', self.kwargs.get('app_key', False))
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
		if user is not None : login(self.request, user)
		return super(Login, self).form_valid(form)

	def get_success_url(self):
		if self.kwargs.get('app_key', False):
			return redirect('auth_network_identify', app_key=self.kwargs['app_key'])
		else :
			return redirect('auth_network_home')

	def get_context_data(self, **kwargs):
		context = super(Login, self).get_context_data(**kwargs)
		context['page_title'] = 'Connexion'
		context['submit_button_text'] = 'Se connecter'
		context['app_key'] = self.kwargs.get('app_key', False)
		context['active_tab'] = reverse('auth_network_login')
		return context



class Register(FormView):

	''' C'est la vue qui permet aux utilisateurs de créer un compte '''
	form_class = UserCreationForm
	template_name = "form.html"
	
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
		if self.kwargs.get('app_key', False):
			return redirect('auth_network_identify', app_key=self.kwargs['app_key'])
		else :
			return redirect('auth_network_home')

	def get_context_data(self, **kwargs):
		context = super(Register, self).get_context_data(**kwargs)
		context['page_title'] = 'Créer un compte'
		context['submit_button_text'] = 'Créer'
		context['app_key'] = self.kwargs.get('app_key', False)
		context['active_tab'] = reverse('auth_network_register')
		return context



@login_required
def UserInfo(request):
	# todo switch to detailview
	return render(request, 'auth_network_provider/user_info.html', {
		'page_title': 'Mon compte',
		'active_tab': reverse('auth_network_user_info'),
		})