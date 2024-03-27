from django import forms
from .models import Appointment, UserProfile, PatientProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    user_type = PatientProfile
  

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class DoctorNurseRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse')])
    specialization = forms.CharField(required=False)  # Optional, shown only if Doctor is selected
    isPartTime = forms.BooleanField(required=False, initial=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'user_type', 'specialization', 'isPartTime')
        
