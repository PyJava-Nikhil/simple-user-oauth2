from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'signup/$', views.Signup.as_view(), name="signup_login"),
	url(r'change_password/$', views.ChangePassword.as_view(), name="change_password"),
]

