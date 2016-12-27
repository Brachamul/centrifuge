from django.contrib import admin

from .models import *



class AppAdmin(admin.ModelAdmin):
	model = App
	readonly_fields = ( "key", "secret", )
	list_display = ("name", "trusted", "set_token_url", "callback_url", )

admin.site.register(App, AppAdmin)


class CredentialsInline(admin.TabularInline):
	model = Credentials
	readonly_fields = ( "app", "user_has_authorized", "token", )
	extra = 0

class NetworkUserAdmin(admin.ModelAdmin):
	model = NetworkUser
	readonly_fields = ("user", "uuid", )
	list_display = ("user", "number_of_apps",)
	inlines = [CredentialsInline, ]

admin.site.register(NetworkUser, NetworkUserAdmin)



class CredentialsAdmin(admin.ModelAdmin):
	model = Credentials
	readonly_fields = ( "token", "date_joined", )

admin.site.register(Credentials, CredentialsAdmin)



