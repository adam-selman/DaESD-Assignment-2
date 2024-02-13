from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    userID = models.AutoField(primary_key=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    isPatient = models.BooleanField(default = False)
    isDoctor = models.BooleanField(default = False)
    isPartTime = models.BooleanField(default = False)
    isNurse = models.BooleanField(default = False)
    isAdmin = models.BooleanField(default = False)
    isNHSTrust = models.BooleanField(default = False)

class ContactInfo(models.Model):
    contactID = models.AutoField(primary_key=True)
    contactType = models.CharField(max_length=100)
    contactValue = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_infos')

class Addresse(models.Model):
    number = models.IntegerField()
    buildingName = models.CharField(max_length=100)
    streetName = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    country = models.CharField(max_length=16)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.TimeField()
    status = models.CharField(max_length=100)
    patientID = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_appointment')
    doctorID = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='doctor_appointment')
    nurseID = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='nurse_appointment')

class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    dateIssued = models.DateField()
    appointmentID = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='invoices')
    patientID = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_invoice')
    billingParty = models.BooleanField()

class Service(models.Model):
    serviceID = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)

class AppointmentService(models.Model):
    appointmentServiceID = models.AutoField(primary_key=True)
    appointmentID = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='appointment_services')
    serviceID = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointment_services')

class DoctorServiceRate(models.Model):
    doctorServiceRateID = models.AutoField(primary_key=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    serviceID = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='doctor_service_rates')

class NurseServiceRate(models.Model):
    nurseServiceRateID = models.AutoField(primary_key=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    serviceID = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='nurse_service_rates')

class Prescription(models.Model):
    prescriptionID = models.AutoField(primary_key=True)
    repeatable = models.BooleanField()
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    instructions = models.CharField(max_length=100)
    issueDate = models.DateField()
    appointmentID = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    doctorID = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='doctor_prescription')
    nurseID = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='nurse_prescription')
    patientID = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_prescription')

class Timetable(models.Model):
    timetableID = models.AutoField(primary_key=True)
    nurseID = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='nurse_timetable')
    doctorID = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='doctor_timetable')
    day = models.CharField(max_length=100)
    startTime = models.TimeField()
    endTime = models.TimeField()
