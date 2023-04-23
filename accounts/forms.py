from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UsernameField, UserCreationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class SmartRelaysPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True, 'class': 'input'}
        ),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'input'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'input'}),
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'class': 'input'})
        self.fields['first_name'].widget = forms.TextInput(attrs={'class': 'input'})
        self.fields['last_name'].widget = forms.TextInput(attrs={'class': 'input'})
        self.fields['email'].widget = forms.EmailInput(attrs={'class': 'input'})

        self.fields['is_staff'].help_text = 'Designates whether the user can log into the Django admin site.'


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(attrs={'class': 'input'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'input'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'input'})
