from django import forms
from .models import Appointment, UserProfile

# class AppointmentBookingForm(forms.Form):
#     your_name = forms.CharField(label="Your name")
#     date = forms.DateField(label="Booking Date")

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