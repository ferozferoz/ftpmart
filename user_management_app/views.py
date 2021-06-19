from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView, UpdateView
from django.contrib.auth import authenticate, login, logout
from .utils import password_reset_token
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from .forms import *
from ecomm_app.views import CartNo
from ecomm_app.models import Order
# Create your views here.

class CustomerRegistrationView(CreateView):
    template_name = "customer_registration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomm_app:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        # subject = 'welcome to CityMart'
        # message = f'Hi {user.username}, thank you for registering in FtpMart.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # send_mail( subject, message, email_from, recipient_list )
        return super().form_valid(form)


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("ecomm_app:home")


class CustomerLoginView(FormView):
    template_name = "customer_login.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomm_app:home")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and usr.customer:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerProfileView(CartNo, TemplateView):
    template_name = "customer_profile.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect("/login/?next=/profile/")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(customer = customer).all()[0:5]
        print(orders)
        context['order_items'] = orders
        return context


class PasswordForgotView(FormView):
    template_name = "forgot_password.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.filter(user__email=email)[0]
        user = customer.user
        text_content = 'Please Click the link below to reset your password. '
        html_content = url + "/password-reset/" + email + \
                       "/" + password_reset_token.make_token(user) + "/"

        send_mail(
            'Password Reset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)

