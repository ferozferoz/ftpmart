from django import forms
from .models import Customer, User
from phonenumber_field.formfields import PhoneNumberField


class CustomerRegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    mobile = PhoneNumberField() # validators should be a list

    class Meta:
        model = Customer
        fields = ["email", "password", "mobile"]

    def clean_username(self):
        uname = self.cleaned_data.get("email")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Customer with this email/username already exists.")
        return uname


class CustomerLoginForm(forms.Form):
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
