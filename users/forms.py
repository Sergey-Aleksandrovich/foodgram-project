from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
                                help_text='Ваш пароль должен содержать как '
                                          'минимум 8 символов.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        labels = {'username': 'Логин',
                  'email': 'Адрес электронной почты',
                  }




