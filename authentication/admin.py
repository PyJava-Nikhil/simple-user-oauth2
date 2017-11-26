from django.contrib import admin
from .models import Account
# Register your models here.


class AuthenticationCustom(admin.ModelAdmin):
	list_display = ("email", "id")

	search_fields = ["email", "mobile"]


admin.site.register(Account, AuthenticationCustom)