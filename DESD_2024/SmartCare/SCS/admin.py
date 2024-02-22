from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.



admin.site.register(DoctorUser)
admin.site.register(NurseUser)
admin.site.register(PatientUser)
admin.site.register(AdminUser)
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
admin.site.register(Allergy)
admin.site.register(UserAllergy)
admin.site.register(Medication)
