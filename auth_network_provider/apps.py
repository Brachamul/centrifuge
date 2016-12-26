from django.apps import AppConfig

class AuthNetworkProviderConfig(AppConfig):
	name = 'auth_network_provider'
	verbose_name = "Network Authentication Provider"

	def ready(self):
		import auth_network_provider.signals