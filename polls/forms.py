from django import forms
from django.core.exceptions import ValidationError

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                password2: ValidationError('Пароли не совпадают', code='password_nisnatch')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'username', 'email')


class UpdateForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватарка', required=False)
    first_name = forms.CharField(label='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    username = forms.CharField(label='Логин', required=False)
    email = forms.CharField(label='Почта', required=False)

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'username', 'email')
