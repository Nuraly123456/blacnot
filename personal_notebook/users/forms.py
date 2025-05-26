from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="Электрондық пошта")

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Пайдаланушы аты',
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio', 'location', 'birth_date', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'profile_image': 'Профиль суреті',
            'bio': 'Биография',
            'location': 'Орналасқан жері',
            'birth_date': 'Туған күні',
            'website': 'Веб-сайт',
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Ескі құпия сөз"
        self.fields['new_password1'].label = "Жаңа құпия сөз"
        self.fields['new_password2'].label = "Жаңа құпия сөзді растау"