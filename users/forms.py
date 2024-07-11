from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email address does not exist.")
        return email

class OTPVerificationForm(forms.Form):
    otp_value = forms.CharField(max_length=10)
 