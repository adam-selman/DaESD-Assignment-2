from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('nurse', 'Nurse'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    
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
    allergies = models.TextField()
    isPrivate = models.BooleanField(default = False)

    def __str__(self):
        return self.user_profile.user.username

class AdminProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete = models.CASCADE, 
                                        related_name = 'admin_user')
     
    class Meta:
        permissions = [
            ("SCS.can_access_my_model_admin_dash", "Can access admin dash" ),
        ]


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
    
    def __str__(self):
        if self.buildingName:
            if self.number:
                return f"{self.number} {self.buildingName}, {self.streetName}, {self.city}, {self.county}, {self.postcode}, {self.country}"
            else:
                return f"{self.buildingName}, {self.streetName}, {self.city}, {self.county}, {self.postcode}, {self.country}"
        else:
            return f"{self.number} {self.streetName}, {self.city}, {self.county}, {self.postcode}, {self.country}"

class Service(models.Model):
    serviceID = models.AutoField(primary_key = True)
    service = models.CharField(max_length = 100)
    description = models.TextField()
    duration = models.IntegerField()
    def __str__(self):
        return self.service

class Appointment(models.Model):
    appointmentID = models.AutoField(primary_key = True)
    service = models.ForeignKey(Service, on_delete = models.CASCADE,
                                related_name = 'appointment_service' )
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=256)
    notes = models.TextField()
    status = models.CharField(max_length=100)
    patient = models.ForeignKey(PatientProfile, on_delete = models.CASCADE, 
                                   related_name = 'patient_appointment')
    doctor = models.ForeignKey(UserProfile, null = True, 
                                        on_delete = models.CASCADE, 
                                        related_name = 'doctor_appointment')
    nurse = models.ForeignKey(UserProfile, null = True,
                                 on_delete = models.CASCADE,
                                 related_name = 'nurse_appointment')
    def __str__(self):
        return str(self.appointmentID)

class Invoice(models.Model):
    invoiceID = models.AutoField(primary_key = True)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    status = models.BooleanField(max_length = 100) # either paid or unpaid
    dateIssued = models.DateTimeField()
    appointment = models.ForeignKey(Appointment, on_delete = models.CASCADE, 
                                         related_name = 'invoices')
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, 
                                related_name='patient_invoice')
    billingParty = models.CharField(max_length = 100, 
                                   choices = [('nhs', 'NHS'),
                                              ('insurance', 'Insurance'), 
                                              ('private', 'Private')])

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
    approved = models.BooleanField()
    medication = models.ForeignKey(Medication, on_delete = models.CASCADE, 
                                   related_name = 'medication_prescription')
    dosage = models.CharField(max_length = 100)
    quantity = models.IntegerField()
    instructions = models.TextField()
    issueDate = models.DateTimeField(default=None)
    reissueDate = models.DateTimeField(null = True)
    appointment = models.ForeignKey(Appointment, on_delete = models.CASCADE, 
                                      related_name = 'prescriptions')
    patient = models.ForeignKey(UserProfile, on_delete = models.CASCADE, 
                                   related_name = 'patient_prescription')
    doctor = models.ForeignKey(UserProfile, null = True, 
                                        on_delete=  models.CASCADE, 
                                        related_name = 'practitioner_prescription')
    nurse = models.ForeignKey(UserProfile, null = True,
                                    on_delete = models.CASCADE,
                                    related_name = 'nurse_prescription')

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

