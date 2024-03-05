from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from charity_app.models import User
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    email = forms.EmailField(label="email", validators=[EmailValidator])
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        self.user = authenticate(email=email, password=password)
        if self.user is None:
            raise ValidationError('Nieprawidlowy login lub haslo')


def validate_email_free(email):

    if User.objects.get(email=email):
        raise ValidationError("Użytkownik o danym adresie email już istnieje")

    # try:
    #     User.objects.get(email=email)
    #
    # except User.DoesExist:
    #     raise ValidationError("Użytkownik o danym adresie email już istnieje")



class UserForm(forms.Form):
    email = forms.EmailField(label="email", validators=[validate_email_free])
    password = forms.CharField(widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Wprowadź ponownie hasło")
    name = forms.CharField(max_length=64, label="Imię")
    surname = forms.CharField(max_length=64, label="Nazwisko")


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('Hasła nie sią identyczne')