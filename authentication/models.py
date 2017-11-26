from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class AccountManager(BaseUserManager):

	def create_user(self, email, password=None, **kwargs):

		if not email:
			return ("Users must have valid email address")

		account = self.model(
			email=email, username=email, mobile=kwargs.get("mobile"))

		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, email, password, **kwargs):

		account = self.create_user(email, password, **kwargs)

		account.is_admin = True
		account.is_superuser = True
		account.is_active = True
		account.is_staff = True
		account.save()

		return account

class Account(AbstractBaseUser, PermissionsMixin):

	email = models.EmailField(unique=True)
	username = models.CharField(max_length=300,unique=True)
	mobile = models.CharField(max_length=11, unique=True)
	name = models.CharField(max_length=100, null=True, blank=True)
	is_active = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	last_login = models.DateTimeField(auto_now_add=True)
	is_superuser = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	objects = AccountManager()

	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ["mobile"]
	
	def get_short_name(self):
		return str(self.email)

	def __str__(self):
		return str(self.email)
