from django.db import models
from django.contrib.auth.models import User

class DoctorUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_user')

class NurseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_user')

class PatientUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_user')

class AdminUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_user')

class ContactInfo(models.Model):
    contactID = models.AutoField(primary_key=True)
    contactType = models.CharField(max_length=100)
    contactValue = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_infos')

class Address(models.Model):
    addressID = models.AutoField(primary_key=True)
    number = models.IntegerField()
    buildingName = models.CharField(max_length=100)
    streetName = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    country = models.CharField(max_length=16)
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key=True)
    dateTime = models.DateTimeField()
    duration = models.TimeField()
    status = models.CharField(max_length=100)
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_appointment')
    practicioner = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='practitioner_appointment')

class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    dateIssued = models.DateField()
    appointmentID = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoices')
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_invoice')
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

class Medication(models.Model):
    medicationID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Prescription(models.Model):
    prescriptionID = models.AutoField(primary_key=True)
    repeatable = models.BooleanField()
    medication = models.ManyToManyField(Medication, related_name='prescriptions')
    dosage = models.CharField(max_length=100)
    instructions = models.CharField(max_length=100)
    issueDate = models.DateField()
    appointmentID = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    practitioner = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='practitioner_prescription')
    patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_prescription')

class Timetable(models.Model):
    timetableID = models.AutoField(primary_key=True)
    nurse = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='nurse_timetable')
    doctor = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='doctor_timetable')
    day = models.CharField(max_length=100)
    startTime = models.TimeField()
    endTime = models.TimeField()

class Allergy(models.Model):
    allergyID = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 100)

class UserAllergy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'allergy']


