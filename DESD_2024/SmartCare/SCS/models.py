from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    user_type = models.CharField(max_length = 10, choices = [('doctor', 'Doctor'),
                                    ('patient', 'Patient'), ('nurse', 'Nurse'),
                                    ('admin', 'Admin')])
    
    def __str__(self):
        return self.user.username

class DoctorProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                        related_name = 'doctor_user')
    specialization = models.CharField(max_length = 100)
    isPartTime = models.BooleanField(default = False)

    def __str__(self):
        return self.user_profile.user.username

class NurseProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, 
                                        related_name = 'nurse_user')

    def __str__(self):
        return self.user_profile.user.username
    
class PatientProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                        related_name = 'patient_user')
    age = models.IntegerField()
    allergies = models.JSONField(default = dict)
    isPrivate = models.BooleanField(default = False)

    def __str__(self):
        return self.user_profile.user.username

class AdminProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                        related_name = 'admin_user')

    def __str__(self):
        return self.user_profile.user.username

class ContactNumber(models.Model):
    contactID = models.AutoField(primary_key = True)
    contactType = models.CharField(max_length = 100, 
                                   choices = [('mobile', 'Mobile'),
                                              ('home', 'Home'), 
                                              ('work', 'Work')])
    contactValue = models.CharField(max_length = 100)
    description = models.CharField(max_length = 100)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, 
                             related_name ='contact_infos')

class Address(models.Model):
    addressID = models.AutoField(primary_key = True)
    number = models.IntegerField(null = True)
    buildingName = models.CharField(max_length = 100, null = True)
    streetName = models.CharField(max_length = 100)
    city = models.CharField(max_length = 100)
    county = models.CharField(max_length = 100)
    postcode = models.CharField(max_length = 8)
    country = models.CharField(max_length = 16)
    description = models.CharField(max_length = 100)
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE, 
                             related_name = 'addresses')

class Service(models.Model):
    serviceID = models.AutoField(primary_key = True)
    service = models.CharField(max_length = 100)
    description = models.TextField()
    duration = models.IntegerField()

class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key = True)
    service = models.ForeignKey(Service, on_delete = models.CASCADE,
                                related_name = 'appointment_service' )
    dateTime = models.DateTimeField()
    duration = models.IntegerField()
    description = models.CharField(max_length=256)
    notes = models.TextField()
    status = models.CharField(max_length=100)
    patient = models.ForeignKey(UserProfile, on_delete = models.CASCADE, 
                                   related_name = 'patient_appointment')
    doctor = models.ForeignKey(UserProfile, null = True, 
                                        on_delete = models.CASCADE, 
                                        related_name = 'doctor_appointment')
    nurse = models.ForeignKey(UserProfile, null = True,
                                 on_delete = models.CASCADE,
                                 related_name = 'nurse_appointment')

class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key = True)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    status = models.CharField(max_length = 100)
    dateIssued = models.DateField()
    appointment = models.OneToOneField(Appointment, on_delete = models.CASCADE, 
                                         related_name = 'invoices')
    patient = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                   related_name = 'patient_invoice')
    billingParty = models.BooleanField()

class DoctorServiceRate(models.Model):
    doctorServiceRateID = models.AutoField(primary_key = True)
    rate = models.DecimalField(max_digits = 10, decimal_places = 2)
    service = models.OneToOneField(Service, on_delete = models.CASCADE, 
                                  related_name = 'doctor_service_rates')

class NurseServiceRate(models.Model):
    nurseServiceRateID = models.AutoField(primary_key = True)
    rate = models.DecimalField(max_digits = 10, decimal_places = 2)
    service = models.OneToOneField(Service, on_delete = models.CASCADE, 
                                  related_name = 'nurse_service_rates')

class Medication(models.Model):
    medicationID = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)

class Prescription(models.Model):
    prescriptionID = models.AutoField(primary_key = True)
    repeatable = models.BooleanField()
    medication = models.ManyToManyField(Medication, related_name = 'prescriptions')
    dosage = models.CharField(max_length = 100)
    instructions = models.TextField()
    issueDate = models.DateField()
    appointment = models.ForeignKey(Appointment, on_delete = models.CASCADE, 
                                      related_name = 'prescriptions')
    practitioner = models.OneToOneField(UserProfile, null = True, 
                                        on_delete=  models.CASCADE, 
                                        related_name = 'practitioner_prescription')
    patient = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                   related_name = 'patient_prescription')

class Timetable(models.Model):
    timetableID = models.AutoField(primary_key = True)
    practitioner = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                        related_name = 'practitioner_timetable')
    monday = models.BooleanField(default = False)
    tuesday = models.BooleanField(default = False)
    wednesday = models.BooleanField(default = False)
    thursday = models.BooleanField(default = False)
    friday = models.BooleanField(default = False)
    saturday = models.BooleanField(default = False)
    sunday = models.BooleanField(default = False)

