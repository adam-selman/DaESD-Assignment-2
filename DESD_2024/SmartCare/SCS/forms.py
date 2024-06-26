from django import forms
from .models import Appointment, UserProfile, PatientProfile, DoctorProfile, NurseProfile, Prescription
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.core.exceptions import ValidationError
import datetime

class CustomDateField(forms.DateField):
    def to_python(self, value):
        if not value:
            return None
        try:
            day, month, year = map(int, value.split('/'))
            return datetime.date(year, month, day)
        except ValueError:
            raise ValidationError('Invalid date format. Use DD/MM/YYYY.')


#form now takes age as required by table to not be null 
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    date_of_birth = CustomDateField(required=True)
    gender = forms.CharField(max_length=10)
    #user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    user_type = PatientProfile
    address_number = forms.IntegerField()
    address_street = forms.CharField(max_length=100, required=True)
    address_city = forms.CharField(max_length=100, required=True)
    address_postcode = forms.CharField(max_length=10, required=True)
    allergies = forms.CharField(max_length=100, required=True)
    isPrivate = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]


class DoctorNurseRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse')])
    specialization = forms.CharField(required=False)  # Optional, shown only if Doctor is selected
    isPartTime = forms.BooleanField(required=False, initial=False)

    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)
    date_of_birth = CustomDateField(required=True)
    gender = forms.CharField(max_length=10)

    address_number = forms.IntegerField()
    address_street = forms.CharField(max_length=100, required=True)
    address_city = forms.CharField(max_length=100, required=True)
    address_postcode = forms.CharField(max_length=10, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]



'''class DoctorNurseRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse')])
    specialization = forms.CharField(required=False)  # Optional, shown only if Doctor is selected
    isPartTime = forms.BooleanField(required=False, initial=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'user_type', 'specialization', 'isPartTime')'''
        
class AppointmentBookingForm(forms.ModelForm):
        fields = UserCreationForm.Meta.fields + ('email', 'user_type', 'specialization', 'isPartTime')


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
