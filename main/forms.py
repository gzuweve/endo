import re

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'placeholder': 'введите пароль'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'placeholder': 'повторите пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("такой email уже зарегистрирован")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # проверка длины
        if len(password) < 8:
            raise ValidationError("пароль должен содержать минимум 8 символов")

        return password

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            "class": "input",  # ваш класс
            "id": "id_username",
            "autocomplete": "username",
            "placeholder": "Введите ваш логин",
            "required": True
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "input",  # ваш класс
            "id": "id_password",
            "autocomplete": "current-password",
            "placeholder": "Введите пароль",
            "required": True
        })
    )
    # чекбокс оставим РАЗМЕТКОЙ в шаблоне (чтобы не дублировался)
    remember = forms.BooleanField(required=False, label="Запомнить меня",
                                  widget=forms.CheckboxInput(attrs={"id": "remember_me"}))




