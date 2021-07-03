# -*- coding: utf-8 -*-
from django import forms
from .models import Order, Customer, User,  Item
from phonenumber_field.formfields import PhoneNumberField


class CheckoutForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = ["full_name", "house_no", "street", "city", "pin_code", "landmark"]

        widgets={

                "full_name": forms.TextInput(attrs={'class':'form-control'}),
                "house_no": forms.TextInput(attrs={'class':'form-control'}),
                "street": forms.TextInput(attrs={'class':'form-control'}),
                "city": forms.TextInput(attrs={'class':'form-control'}),
                "pin_code": forms.TextInput(attrs={'class': 'form-control'}),
                "land_mark": forms.TextInput(attrs={'class': 'form-control'})

        }


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))

    class Meta:
        model = Item
        fields = ["name", "slug", "category","sub_category", "image", "cost_price",
                  "display_original_selling_price","display_new_selling_price", "description", "warranty", "return_policy","supplier"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"
            }),
            "sub_category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product..."
            }),
            "display_original_selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "display_new_selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Description of the product...",
                "rows": 5
            }),
            "warranty": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product warranty here..."
            }),
            "return_policy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product return policy here..."
            }),
            "supplier": forms.Select(attrs={
                "class": "form-control"
            }),

        }
