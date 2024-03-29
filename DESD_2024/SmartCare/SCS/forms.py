from django import forms
from .models import Appointment, UserProfile, PatientProfile, DoctorProfile, NurseProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_type = self.cleaned_data.get('user_type')

            # Create or update the UserProfile instance.
            user_profile, _ = UserProfile.objects.update_or_create(
                user=user, defaults={'user_type': user_type}
            )

            if user_type == 'doctor':
                # Check explicitly for an existing DoctorProfile.
                doctor_profile = DoctorProfile.objects.filter(user_profile=user_profile).first()
                if doctor_profile:
                    # Update existing DoctorProfile.
                    doctor_profile.specialization = self.cleaned_data.get('specialization')
                    doctor_profile.isPartTime = self.cleaned_data.get('isPartTime')
                    doctor_profile.save()
                else:
                    # Create a new DoctorProfile.
                    DoctorProfile.objects.create(
                        user_profile=user_profile,
                        specialization=self.cleaned_data.get('specialization'),
                        isPartTime=self.cleaned_data.get('isPartTime')
                    )

            elif user_type == 'nurse':
                # Ensure only one NurseProfile exists for the UserProfile.
                NurseProfile.objects.get_or_create(user_profile=user_profile)

        return user



'''class DoctorNurseRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('doctor', 'Doctor'), ('nurse', 'Nurse')])
    specialization = forms.CharField(required=False)  # Optional, shown only if Doctor is selected
    isPartTime = forms.BooleanField(required=False, initial=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'user_type', 'specialization', 'isPartTime')'''
        
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