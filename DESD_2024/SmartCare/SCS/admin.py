from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile,DoctorProfile,NurseProfile,AdminProfile,PatientProfile, ContactInfo, Address, Appointment, Invoice

# Register your models here.

admin.site.register( PatientProfile)
admin.site.register( DoctorProfile)
admin.site.register( NurseProfile)
admin.site.register( AdminProfile)
admin.site.register(UserProfile)
admin.site.register(ContactInfo)
admin.site.register(Address)
admin.site.register(Appointment)
admin.site.register(Invoice)
