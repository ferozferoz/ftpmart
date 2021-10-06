from django import forms
from django.core.validators import RegexValidator

from ecomm_app.models import Customer, User


class RegistrationForm(forms.Form):

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10,13}$', message="Phone number must have 10 phone digits, you can add +91 for mobile")
    phone_number = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),validators=[phone_regex], max_length=13)  # validators should be a list

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    re_enter_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        uname = self.cleaned_data.get("email")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this email/username already exists.")
        return uname

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        pwd_1 = self.cleaned_data.get("password")
        if pwd !=pwd_1 :
            raise forms.ValidationError(
                "Password do not match, re-enter")
        return pwd


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter the email used in customer account..."
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError(
                "Customer with this account does not exists..")
        return e


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = ["full_name", "house_no", "street", "city", "pin_code", "landmark", "mobile"]

        widgets = {

                "full_name": forms.TextInput(attrs={'class':'form-control'}),
                "house_no": forms.TextInput(attrs={'class':'form-control'}),
                "street": forms.TextInput(attrs={'class':'form-control'}),
                "city": forms.TextInput(attrs={'class':'form-control'}),
                "pin_code": forms.TextInput(attrs={'class': 'form-control'}),
                "land_mark": forms.TextInput(attrs={'class': 'form-control'}),
                "mobile": forms.TextInput(attrs={'class': 'form-control'})

        }
