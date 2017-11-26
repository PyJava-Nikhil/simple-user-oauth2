from django.shortcuts import render
from .models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauthlib.common import generate_token
import traceback
import base64
from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.timezone import timedelta
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
# Create your views here.

def token_json(token):
	access_token = {
	"token":token.token,
	"scope":"read write",
	"expires":36000,
	"token_type":"Bearer"
	}
	return access_token

def get_token(user):
	app = Application.objects.get(user=user)
	token = generate_token()
	refresh_token = generate_token()

	access_token = AccessToken.objects.create(
		application=app,
		user=user,
		token=token,
		scope="read write",
		expires=timezone.now()+timedelta(seconds=36000)
		)

	RefreshToken.objects.create(
		application=app,
		user=user,
		access_token=access_token,
		token=refresh_token,
		)
	print(access_token)
	return token_json(access_token)

class Signup(APIView):

	def post(self, request):
		try:
			data = request.data
			name = data["name"]
			email = data["email"]
			mobile = data["mobile"]
			password = data["password"]

			try:
				account = Account.objects.get(mobile=mobile)
				return Response({"is_mobile_exist":True},status=400)
			except:
				pass

			try:
				account = Account.objects.get(email=email)
				return Response({"is_email_exist":True},status=400)
			except:
				pass

			account = Account.objects.create(
				name=name,
				email=email,
				mobile=mobile,
				is_active=True
				)
			Application.objects.create(user=account, client_type=Application.CLIENT_CONFIDENTIAL, authorization_grant_type=Application.GRANT_PASSWORD)
			account.set_password(password)
			account.save()
			return Response({"success":True, "acc_id":account.id},status=201)
		except Exception as e:
			traceback.print_exc()
			return Response({"error":str(e)},status=400)

	def get(self, request):

		try:
			encoded_data = request.META.get("HTTP_AUTHORIZATION").split(' ')[1]
			username = base64.b64decode(encoded_data).decode('utf-8').partition(':')[0]
			password = base64.b64decode(encoded_data).decode('utf-8').partition(':')[2]
			
			user = authenticate(username=username, password=password)

			if user:
				token = get_token(user)
				print(token)
				return Response({"token":token, "id":user.id},status=200)
			return Response({"error":True},status=400)
		except Exception as e:
			traceback.print_exc()
			return Response({"error":str(e)},status=400)


class ChangePassword(APIView):
	permission_classes = [TokenHasReadWriteScope]
	
	def post(self, request):
		try:
			user = request.user
			data = request.data
			password = data["password"]
			print(user, ">>>>>>>>>>>")
			if len(str(password).strip())<6:
				return Response({"invalid_password":True},status=400)
			account_obj = Account.objects.get(email=user, is_active=True)
			account_obj.set_password(str(password).strip())
			account_obj.save()
			return Response({"success":True},status=400)
		except Exception as e:
			traceback.print_exc()
			return Response({"error":str(e)},status=400)