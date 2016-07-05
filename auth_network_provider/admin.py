from django.contrib import admin

from .models import *



class AppAdmin(admin.ModelAdmin):
	model = App
	readonly_fields = ( "key", "secret", )

admin.site.register(App, AppAdmin)



class UserAdmin(admin.ModelAdmin):
	model = User
	readonly_fields = ( "password", "last_login", "date_joined", )

admin.site.register(User, UserAdmin)



class CredentialsAdmin(admin.ModelAdmin):
	model = Credentials
	readonly_fields = ( "token", "date_joined", )

admin.site.register(Credentials, CredentialsAdmin)