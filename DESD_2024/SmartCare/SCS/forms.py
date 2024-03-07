from django import forms
from .models import Appointment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "user_type"]

        
class AppointmentBookingForm(forms.ModelForm):
    """
    Form object for booking patient appointments

    Args:
        forms (django.forms): Django implementation of forms
    """

    class Meta:
        model = Appointment
        fields = ['service', 'dateTime', 'duration', 'description', 'notes', 'status']
        widgets = {'dateTime': forms.widgets.DateInput(attrs={'type': 'date'})}



# class AppointmentBookingForm(forms.Form):
#     your_name = forms.CharField(label="Your name")
#     date = forms.DateField(label="Booking Date")