from django import forms 
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth import password_validation


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-default'}),
        required=True, 
        min_length=3,
        error_messages={
            'required':'O primeiro nome é Obrigatório'
    })
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input-default'}),
        required=True, 
        min_length=3,
        error_messages={
            'required':'O útimo nome é Obrigatório'
    })

    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'input-default w100',}),
        required=True, 
        error_messages={
            'required':'O e-mail é Obrigatório'
        }
    )

    password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-default w100',}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )

    password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input-default w100',}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )

    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-default w100',}),
            'email':  forms.TextInput(attrs={'class': 'input-default w100',}),       
        }