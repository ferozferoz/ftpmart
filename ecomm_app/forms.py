# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from .models import Customer,User
from django.core.validators import RegexValidator


class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = ["full_name", "house_no", "street", "city", "pin_code", "landmark"]

        widgets={

                "full_name": forms.TextInput(attrs={'class': 'form-control'}),
                "house_no": forms.TextInput(attrs={'class': 'form-control'}),
                "street": forms.TextInput(attrs={'class': 'form-control'}),
                "city": forms.TextInput(attrs={'class': 'form-control'}),
                "pin_code": forms.TextInput(attrs={'class': 'form-control'}),
                "landmark": forms.TextInput(attrs={'class': 'form-control'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        full_name = cleaned_data.get("full_name")
        house_no = cleaned_data.get("house_no")
        street = cleaned_data.get("street")
        city = cleaned_data.get("city")
        pin_code = cleaned_data.get("pin_code")
        landmark = cleaned_data.get("landmark")

        if full_name is None:
            raise ValidationError(
                "full name cannot be empty"
            )
        if house_no is None:
            raise ValidationError(
                "house number cannot be empty"
            )
        if street is None:
            raise ValidationError(
                "street cannot be empty"
            )
        if city is None:
            raise ValidationError(
                "city cannot be empty"
            )
        if pin_code is None:
            raise ValidationError(
                "pin code cannot be empty"
            )
        if landmark is None:
            raise ValidationError(
                "landmark cannot be empty"
            )


class RegistrationForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
            validators=[RegexValidator(regex=r'^\+?1?\d{10,13}$',
            message="Phone number must have 10 phone digits, you can add +91 for mobile")], max_length=13)  # validators should be a list

    def clean_email(self):
        uname = self.cleaned_data.get("email")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this email/username already exists.")
        return uname

    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if Customer.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError(
                "Mobile number already exists in database")
        return mobile




