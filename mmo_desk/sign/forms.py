from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group
from publication.models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, request, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        return user



class ValidationEmailForm(forms.ModelForm):
    confirmation_code = forms.CharField(label='Код подтверждения', max_length=20)

    class Meta:
        model = Profile
        fields = ('confirmation_code',)

