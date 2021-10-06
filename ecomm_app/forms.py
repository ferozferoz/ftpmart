# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from .models import Customer
from phonenumber_field.formfields import PhoneNumberField


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

