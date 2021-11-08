# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from .models import Item , Category, Supplier,Warranty,ReturnPolicy
from phonenumber_field.formfields import PhoneNumberField

class WarrantyForm(forms.ModelForm):

    class Meta:
        model = Warranty
        fields = ["warranty_type", "warranty_desc"]
        widgets = {
                "warranty_type": forms.TextInput(attrs={'class':'form-control'}),
                "warranty_desc": forms.TextInput(attrs={'class':'form-control'}),
        }


class ReturnPolicyForm(forms.ModelForm):
    class Meta:
        model = ReturnPolicy
        fields = ["return_policy_type", "return_policy_desc"]
        widgets = {
            "return_policy_type": forms.TextInput(attrs={'class': 'form-control'}),
            "return_policy_desc": forms.TextInput(attrs={'class': 'form-control'}),

        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "parent"]
        widgets = {
                "name": forms.TextInput(attrs={'class':'form-control'}),
                "parent": forms.Select(attrs={'class':'form-control'}),
        }


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier
        fields = ["name", "address", "home_phone", "office_phone"]
        widgets = {

                "name": forms.TextInput(attrs={'class':'form-control'}),
                "address": forms.TextInput(attrs={'class': 'form-control'}),
                "home_phone": forms.TextInput(attrs={'class': 'form-control'}),
                "office_phone": forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ["name", "category","sub_category", "image_1", "image_2", "image_3", "image_4", "image_5",
                  "cost_price", "display_original_selling_price", "display_new_selling_price", "description",
                  "warranty", "return_policy", "supplier", "is_active", "availability"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder":  "Enter the product title here..."
            }),
            "category": forms.Select(attrs={
                "class": "form-control"

            }),
            "sub_category": forms.Select(attrs={
                "class": "form-control"
            }),
            "image_1": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "image_2": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "image_3": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "image_4": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "image_5": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "cost_price": forms.NumberInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Marked price of the product..."
            }),
            "display_original_selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Selling price of the product..."
            }),
            "display_new_selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Selling price of the product..."
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Description of the product...",
                "rows": 5
            }),

            "warranty": forms.Select(attrs={
                "class": "form-control"

            }),
            "return_policy": forms.Select(attrs={
                "class": "form-control"

            }),
            "supplier": forms.Select(attrs={
                "class": "form-control"
            }),


        }
