from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Doctor

class DoctorCreationForm(UserCreationForm):
    class Meta:
        model = Doctor
        fields = ["username", "first_name", "last_name", "password1", "password2", "email", "gender", "speciality"]

    gender = forms.ChoiceField(
        choices=Doctor.GENDER_CHOICES,
        label='Gender',
        widget=forms.Select
    )

    speciality = forms.ChoiceField(
        choices=Doctor.SPECIALITY_CHOICES,
        label='Specialty',
        widget=forms.Select
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
