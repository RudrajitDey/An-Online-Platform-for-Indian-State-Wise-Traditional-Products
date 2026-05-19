from django import forms
from django.core.exceptions import ValidationError

from .models import Account, UserProfile
import re


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField(required=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # Minimum length
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters")

        # At least one uppercase
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter")

        # At least one lowercase
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter")

        # At least one digit
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one number")

        # At least one special character
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character")

        return password


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


def _validate_strong_password(password):
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters')
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    if not re.search(r'[a-z]', password):
        raise ValidationError('Password must contain at least one lowercase letter')
    if not re.search(r'[0-9]', password):
        raise ValidationError('Password must contain at least one number')
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character')


class AccountProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'account-input'}),
            'last_name': forms.TextInput(attrs={'class': 'account-input'}),
            'username': forms.TextInput(attrs={'class': 'account-input'}),
            'phone_number': forms.TextInput(attrs={'class': 'account-input'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        qs = Account.objects.filter(username__iexact=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('This username is already taken.')
        return username


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar',
            'bio',
            'date_of_birth',
            'gender',
            'address_line1',
            'address_line2',
            'city',
            'state',
            'country',
            'pincode',
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'account-input-file', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'account-input'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'account-input'}),
            'gender': forms.Select(attrs={'class': 'account-input'}),
            'address_line1': forms.TextInput(attrs={'class': 'account-input'}),
            'address_line2': forms.TextInput(attrs={'class': 'account-input'}),
            'city': forms.TextInput(attrs={'class': 'account-input'}),
            'state': forms.TextInput(attrs={'class': 'account-input'}),
            'country': forms.TextInput(attrs={'class': 'account-input'}),
            'pincode': forms.TextInput(attrs={'class': 'account-input'}),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput(attrs={'class': 'account-input', 'autocomplete': 'current-password'}),
    )
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'class': 'account-input', 'autocomplete': 'new-password'}),
    )
    confirm_password = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput(attrs={'class': 'account-input', 'autocomplete': 'new-password'}),
    )

    def clean_new_password(self):
        pwd = self.cleaned_data.get('new_password')
        if pwd:
            _validate_strong_password(pwd)
        return pwd

    def clean(self):
        data = super().clean()
        new = data.get('new_password')
        confirm = data.get('confirm_password')
        if new and confirm and new != confirm:
            raise ValidationError('New passwords do not match.')
        return data
