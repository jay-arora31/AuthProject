# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator
User = get_user_model()




class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label='Password',
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="Password must be at least 8 characters long, include uppercase and lowercase letters, at least one number, and at least one special character."
            ),
        ]
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if both passwords match
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use. Please choose another one.")
        return email
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Email', max_length=254)
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 p-2',
            'placeholder': 'Enter your email address'
        })
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Old Password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm New Password'})
    )
    


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput,
        min_length=8,
        required=True,
        help_text=_('At least 8 characters long, include uppercase and lowercase letters, at least one number, and at least one special character.')
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput,
        required=True,
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        validate_password(new_password)  # Validate the new password
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError(_('Passwords do not match. Please try again.'))

        return cleaned_data