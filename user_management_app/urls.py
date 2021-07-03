# -*- coding: utf-8 -*-

from django.urls import path
from .views import *

app_name= "user_management_app"

urlpatterns = [

        path("register/", CustomerRegistrationView.as_view(), name="customer_registration"),
        path("logout/", CustomerLogoutView.as_view(), name="customer_logout"),
        path("login/", CustomerLoginView.as_view(), name="customer_login"),
        path("profile/", CustomerProfileView.as_view(), name="customer_profile"),
        path("profile_edit", editCustomerProfileView, name="edit_customer_profile"),
        path("forgot-password/", PasswordForgotView.as_view(), name="password_forgot"),

]
