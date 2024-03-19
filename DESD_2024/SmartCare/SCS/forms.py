from django import forms
from .models import Appointment, UserProfile, PatientProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#form now takes age as required by table to not be null 
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    age = forms.IntegerField(required=True)
    user_type = 'patient' #Tim's fix :P
  
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "age"]

class DoctorNurseRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse')])
    specialization = forms.CharField(required=False)  # Optional, shown only if Doctor is selected
    isPartTime = forms.BooleanField(required=False, initial=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'user_type', 'specialization', 'isPartTime')
        
class AppointmentBookingForm(forms.ModelForm):
    """
    Form object for booking patient appointments
    """

    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'duration', 'description', 'notes', 'status']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'time': forms.widgets.TimeInput(attrs={'type': 'time'}), 
        }




# class AppointmentBookingForm(forms.Form):
#     your_name = forms.CharField(label="Your name")
#     date = forms.DateField(label="Booking Date")