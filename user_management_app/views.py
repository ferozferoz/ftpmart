from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView, ListView, UpdateView
from django.contrib.auth import authenticate, login, logout
from .utils import password_reset_token
from django.conf import settings
from django.core.mail import send_mail
from .forms import *
from ecomm_app.models import Customer, User
import random
import http


# Create your views here.
"""
class RegistrationView(FormView):

    template_name = "ecomm_app/customer_registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("ecomm_app:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        phone_number = form.cleaned_data.get("phone_number")
        user = User.objects.create_user(username, email, password)
        Customer.objects.create(user=user,mobile = phone_number)
        login(self.request, user)
        # code to send meassage
        # subject = 'welcome to CityMart'
        # message = f'Hi {user.username}, thank you for registering in FtpMart.'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user.email, ]
        # send_mail( subject, message, email_from, recipient_list )
        return super().form_valid(form)

"""
class LogoutView(View):

    redirect_url="ecomm_app:home"

    def get(self, request):
        logout(request)
        return redirect(self.redirect_url)



class LoginView(FormView):

    template_name = "user_management_app/customer_login.html"
    form_class = LoginForm
    success_url = reverse_lazy("ecomm_app:home")

    def form_valid(self, form):
        user_name = form.cleaned_data.get("username")
        password = form.cleaned_data["password"]
        user = authenticate(username=user_name, password=password)
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})

        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url

class PasswordForgotView(FormView):

    template_name = "user_management_app/forgot_password.html"
    form_class = PasswordForgotForm
    success_url = "/forgot-password/?m=s"

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get("email")
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        user = User.objects.get(user__email=email)

        text_content = 'Please Click the link below to reset your password. \n'
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


def register(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        if Customer.objects.filter(mobile=mobile).exists():
            context = {'message':'The user with mobile number already exists'}
            return render(request, 'customer_registration.html',context)
        else:
            if User.objects.filter(username=email).exists():
                context = {'message': 'The user with email already exists'}
                return render(request, 'customer_registration.html',context)
            else:

                otp = str(random.randint(1000, 9999))
                #send_otp(mobile,otp)
                request.session['mobile'] = mobile
                request.session['email'] = email
                request.session['name'] = name
                request.session['otp'] = otp
                return redirect("user_management_app:register_otp")

    return render(request,'user_management_app/customer_registration.html')

def register_otp(request):

    context = {'otp':request.session['otp']}

    if request.method == 'POST':
        key = request.POST.get('otp')
        if key == request.session['otp']:
            user = User(username=request.session['email'], email=request.session['email'] ,first_name=request.session['name'])
            user.save()
            customer = Customer(user=user, mobile=request.session['mobile'])
            customer.save()
            login(request, user)
            return redirect("ecomm_app:home")

    return render(request, 'user_management_app/otp.html', context)


def send_otp(mobile , otp):
    print("FUNCTION CALLED")
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.AUTH_KEY
    headers = {'content-type': "application/json" }
    url = "http://control.msg91.com/api/sendotp.php?otp="+otp+"&message="+"Your otp is "+otp +"&mobile="+mobile+"&authkey="+authkey+"&country=91"
    conn.request("GET", url , headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None


def login_otp(request):

    if request.method == 'POST':
        key = request.POST.get('otp')

        if key == request.session['otp']:
            customer = Customer.objects.get(mobile=request.session['mobile'])
            login(request, customer.user)

            if "next" in request.GET:
                next_url = request.GET.get("next")
                return redirect(next_url)
            else:
                return redirect("ecomm_app:home")

        else:

            context = {'message': 'Wrong OTP', 'class': 'danger', 'mobile': request.session['mobile']}
            return render(request, 'user_management_app/login_otp.html', context)

    return render(request, 'user_management_app/login_otp.html',context={'otp':request.session['otp']})


def login_attempt(request):

    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        user = Customer.objects.filter(mobile=mobile).first()

        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'user_management_app/login.html', context)
        otp = str(random.randint(1000, 9999))
        request.session['otp'] = otp
        #send_otp(mobile, otp)
        request.session['mobile'] = mobile
        return redirect('user_management_app:login_otp')

    return render(request, 'user_management_app/login.html')