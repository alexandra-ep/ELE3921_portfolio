from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name= forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]

class BookingForm(forms.Form):
    confirm = forms.BooleanField(required=True)

class CancelBookingForm(forms.Form):
    confirm_cancel = forms.BooleanField(required=True)