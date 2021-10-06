# -*- coding: utf-8 -*-

from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name= "user_management_app"

urlpatterns = [

        #path("register/", RegistrationView.as_view(), name="registration"),
        path("logout/", LogoutView.as_view(), name="logout"),
        #path("login/", LoginView.as_view(), name="login"),

        path("forgot-password/", PasswordForgotView.as_view(), name="password_forgot"),
        path("login/", login_attempt, name="login"),
        path("login_otp/", login_otp, name="login_otp"),
        path("register/", register, name="registration"),
        path("otp/", register_otp, name="register_otp"),

]
