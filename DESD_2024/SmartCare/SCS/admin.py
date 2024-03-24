from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, DoctorProfile, NurseProfile, PatientProfile,\
    AdminProfile, ContactNumber, Address, Appointment, Invoice, Service,\
    DoctorServiceRate, NurseServiceRate, Medication, Prescription, Timetable

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
  list_display = ( "appointmentID","service","date","time","description","notes","status","patient","doctor","nurse",)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(UserProfile)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(PatientProfile)
admin.site.register(AdminProfile)
admin.site.register(ContactNumber)
admin.site.register(Address)
admin.site.register(Invoice)

class ServiceAdmin(admin.ModelAdmin):
  list_display = ( "serviceID", "service","duration","description",)
admin.site.register(Service,ServiceAdmin)
admin.site.register(DoctorServiceRate)
admin.site.register(NurseServiceRate)
admin.site.register(Prescription)
admin.site.register(Timetable)
admin.site.register(Medication)
