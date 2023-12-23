from django.contrib.auth.forms import UserCreationForm
from . import constants
from django import forms
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.CharField(max_length=10, choices=constants.GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name", "email",
                  "account_type", "gender", "birth_date", "city", "postal_code", "country", "street_address"]

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            birth_date = self.cleaned_data['birth_date']
            gender = self.cleaned_data['gender']
            street_address = self.cleaned_data['street_address']
            city = self.cleaned_data['city']
            postal_code = self.cleaned_data['postal_code']
            country = self.cleaned_data['country']
