from django import forms
from .models import Appointment, UserProfile, PatientProfile, Prescription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    #user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    user_type = PatientProfile
  

    class Meta:
        model = User
        fields = ["firstname", "lastname", "username", "email", "password1", "password2"]

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

class PrescriptionForm(forms.ModelForm):
    """
    Form object for creating prescriptions
    """

    class Meta:
        model = Prescription
        fields = ['repeatable', 'approved', 'medication', 'dosage', 'quantity', 'instructions', 'issueDate', 'reissueDate', 'appointment', 'patient', 'doctor', 'nurse']
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
            'time': forms.widgets.TimeInput(attrs={'type': 'time'}), 
        }

    def __init__(self, *args, **kwargs):
        super(PrescriptionForm, self).__init__(*args, **kwargs)
        self.fields['issueDate'].required = False
        self.fields['reissueDate'].required = False
        self.fields['doctor'].required = False
        self.fields['nurse'].required = False
