from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ("username", "email", "display_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            profile = user.profile
            profile.display_name = self.cleaned_data["display_name"]
            profile.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("display_name", "avatar")
