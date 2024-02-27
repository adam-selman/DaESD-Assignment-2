from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.




admin.site.register(UserProfile)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(PatientProfile)
admin.site.register(AdminProfile)
admin.site.register(ContactInfo)
admin.site.register(Address)
admin.site.register(Appointment)
admin.site.register(Invoice)
admin.site.register(Service)
admin.site.register(AppointmentService)
admin.site.register(DoctorServiceRate)
admin.site.register(NurseServiceRate)
admin.site.register(Prescription)
admin.site.register(Timetable)
admin.site.register(Medication)
