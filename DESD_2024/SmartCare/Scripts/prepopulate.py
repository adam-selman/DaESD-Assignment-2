
import csv
import django
from datetime import datetime
import os
import sys

projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, User

from SCS.models import User, UserProfile, DoctorProfile, NurseProfile,\
      PatientProfile, AdminProfile, ContactNumber, Address, Service,\
      DoctorServiceRate, NurseServiceRate, Medication, Appointment,\
      Prescription, Invoice, Timetable

def parse_bool(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        raise ValueError(f"Invalid boolean value: {value}")

def parse_int(value):
    return int(value) if value.strip() else None
    
def open_csv(file):
    try:
        filePath = os.path.join(projectDirectory, file)
        file = open(filePath, 'r')
        return csv.DictReader(file)
    except FileNotFoundError:
        print(f"File {file} not found")
        return None
    
def get_user_by_id(user_id):
    try:
        return User.objects.get(userID = user_id)
    except User.DoesNotExist:
        print(f"User with ID {user_id} does not exist")
        return None
    
def get_user_profile(user_id):
    try:
        return UserProfile.objects.get(pk=int(user_id))
    except UserProfile.DoesNotExist:
        return None
    
def get_patient_profile(user_id):
    try:
        return PatientProfile.objects.get(pk=int(user_id))
    except PatientProfile.DoesNotExist:
        return None 
    
def check_duplicate_user(username):
    try:
        User.objects.get(username = username)
        return True
    except User.DoesNotExist:
        return False

def populate_users(csvFileName, userType, profileClass, additionalFields):
    reader = open_csv(csvFileName)
    if not reader:
        return
    
    for row in reader:
        try:
            username = row.get('username')
            if check_duplicate_user(username):
                print(f"User with username {username} already exists, skipping.")
                continue

            commonFields = {
                'username': username,
                'password': row.get('password'),
                'first_name': row.get('first_name'),
                'last_name': row.get('last_name'),
                'email': row.get('email'),
                'date_joined': timezone.now()
            }

            date_of_birth = row.get('date_of_birth')
            gender = row.get('gender')

            specificFields = {field: row.get(field) for field in additionalFields}
            if additionalFields:
                for field in additionalFields:
                    value = row.get(field)
                    if value.lower() in {'true', 'false'}:
                        specificFields[field] = parse_bool(value)
                    else:
                        specificFields[field] = value

            user = User.objects.create_user(**commonFields)
            
            userProfile = UserProfile.objects.create(user=user, user_type=userType, date_of_birth=date_of_birth, gender=gender)
            
            specificProfile = profileClass.objects.create(user_profile=userProfile, **specificFields)
            
            print(f"{userType} {row['first_name']} {row['last_name']} created")
        except Exception as e:
            print(f"Error creating {userType}:", e)


def populate_services(csvFileName, modelClass, columnToPrint=None, ignore_service=False):
    reader = open_csv(csvFileName)
    if not reader:
        return

    csvFieldName = reader.fieldnames

    if not csvFieldName:
        print(f"File {csvFileName} is empty")
        return

    fieldMapping = {csvFieldName: csvFieldName for csvFieldName in csvFieldName}

    for row in reader:
        objData = {}
        for csvFieldName, djangoFieldName in fieldMapping.items():
            objData[djangoFieldName] = row[csvFieldName]

        try:
            if not ignore_service and 'service' in objData:
                serviceId = objData['service']
                service = Service.objects.get(pk=int(serviceId))

                existingEntry = modelClass.objects.filter(service_id=service).first()
                if existingEntry:
                    print(f"{modelClass.__name__} for {service.service} already exists, skipping.")
                    continue

                objData['service'] = service

            if ignore_service:
                existing_service = Service.objects.filter(service=objData['service']).exists()
                if existing_service:
                    print(f"Skipping duplicate service {objData['service']}")
                    continue

            obj = modelClass.objects.create(**objData)

            if columnToPrint is not None:
                if columnToPrint and columnToPrint in row:
                    valueToPrint = row.get(columnToPrint)
                    print(f"{modelClass.__name__} {valueToPrint} created")
            else:
                print(f"{modelClass.__name__} created")
        except Exception as e:
            print(f"Error creating {modelClass.__name__}:", e)


def populate_contact(csvFileName, modelClass):
    reader = open_csv(csvFileName)
    if not reader:
        return

    csvFieldName = reader.fieldnames

    if not csvFieldName:
        print(f"File {csvFileName} is empty")
        return

    fieldMapping = {csvFieldName: csvFieldName for csvFieldName in csvFieldName}

    for row in reader:
        objData = {}
        for csvFieldName, djangoFieldName in fieldMapping.items():
            fieldValue = row[csvFieldName]

            if isinstance(modelClass._meta.get_field(djangoFieldName), models.IntegerField):
                fieldValue = parse_int(fieldValue)

            objData[djangoFieldName] = fieldValue

        try:
            if 'user' in objData:
                userId = objData['user']
                userProfile = UserProfile.objects.get(pk=int(userId))
                userName = userProfile.user.username

                objData['user'] = userProfile

            existing_entries = modelClass.objects.filter(user=userProfile)
            if existing_entries.exists():
                for entry in existing_entries:
                    if modelClass == Address and entry.postcode == objData.get('postcode'):
                        print(f"Skipping duplicate {modelClass.__name__} for user {userName}")
                        break
                    elif modelClass == ContactNumber and entry.contactValue == objData.get('contactValue'):
                        print(f"Skipping duplicate {modelClass.__name__} for user {userName}")
                        break
                else:
                    obj = modelClass.objects.create(**objData)
                    print(f"{modelClass.__name__} created for user {userName}")
            else:
                obj = modelClass.objects.create(**objData)
                print(f"{modelClass.__name__} created for user {userName}")
        except Exception as e:
            print(f"Error creating {modelClass.__name__}:", e)


def populate_medication(csvFileName, modelClass, columnToPrint=None):
    reader = open_csv(csvFileName)
    if not reader:
        return

    csvFieldName = reader.fieldnames

    if not csvFieldName:
        print(f"File {csvFileName} is empty")
        return

    fieldMapping = {csvFieldName: csvFieldName for csvFieldName in csvFieldName}

    for row in reader:
        objData = {}
        for csvFieldName, djangoFieldName in fieldMapping.items():
            objData[djangoFieldName] = row[csvFieldName]

        try:
            existingMedication = modelClass.objects.filter(name=objData['name']).exists()
            if existingMedication:
                print(f"Skipping duplicate medication {objData['name']}")
                continue

            obj = modelClass.objects.create(**objData)
            if columnToPrint is not None:
                if columnToPrint in row:
                    valueToPrint = row.get(columnToPrint)
                    print(f"{modelClass.__name__} {valueToPrint} created")
            else:
                print(f"{modelClass.__name__} created")
        except Exception as e:
            print(f"Error creating {modelClass.__name__}:", e)



def populate_appointment(csvFileName, modelClass):
    reader = open_csv(csvFileName)
    if not reader:
        return

    if not reader.fieldnames:
        print(f"File {csvFileName} is empty")
        return

    for row in reader:
        objData = {}
        for csvFieldName, fieldValue in row.items():
            if fieldValue.lower() == 'null':
                fieldValue = None

            if isinstance(modelClass._meta.get_field(csvFieldName), models.IntegerField):
                fieldValue = parse_int(fieldValue)

            objData[csvFieldName] = fieldValue

        try:
            '''if 'dateTime' in objData:
                dateTimeStr = objData['dateTime']
                dateTime = datetime.strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S')
                dateTime = timezone.make_aware(dateTime)
                objData['dateTime'] = dateTime'''

            if 'service' in objData:
                serviceId = objData['service']
                service = Service.objects.get(pk=int(serviceId))
                objData['service'] = service

            if 'duration' in objData:
                durationId = objData['duration']
                duration = Service.objects.get(pk=int(durationId))
                objData['duration'] = duration

            existingAppointment = modelClass.objects.filter(date = objData['date'], time = objData['time'], patient = objData['patient']).exists()
            if existingAppointment:
                print(f"Skipping duplicate appointment for patient {objData['patient']} with date issued {objData['date']} and time {objData['time']} ")
                continue

            if 'patient' in objData:
                patient_profile = get_patient_profile(objData['patient'])
                objData['patient'] = patient_profile

            if 'doctor' in objData:
                doctorId = objData['doctor']
                if doctorId is not None:
                    doctor_profile = get_user_profile(objData['doctor'])
                    objData['doctor'] = doctor_profile
                else:
                    objData['doctor'] = None

            if 'nurse' in objData:
                nurseId = objData['nurse']
                if nurseId is not None:
                    nurse_profile = get_user_profile(objData['nurse'])
                    objData['nurse'] = nurse_profile
                else:
                    objData['nurse'] = None

            obj = modelClass.objects.create(**objData)
            print(f"{modelClass.__name__} created for user {objData.get('patient', 'Unknown')}")
        except Exception as e:
            print(f"Error creating {modelClass.__name__}:", e)

def populate_prescription(csvFileName, modelClass):
    reader = open_csv(csvFileName)
    if not reader:
        return

    if not reader.fieldnames:
        print(f"File {csvFileName} is empty")
        return

    for row in reader:
        objData = {}
        for csvFieldName, fieldValue in row.items():
            if fieldValue == 'NULL':
                fieldValue = None
            if fieldValue == 'TRUE' or fieldValue == 'FALSE':
                fieldValue = parse_bool(fieldValue)
            
            if isinstance(modelClass._meta.get_field(csvFieldName), models.IntegerField):
                fieldValue = parse_int(fieldValue)

            objData[csvFieldName] = fieldValue

        try:
            if 'issueDate' in objData:
                issueDateStr = objData['issueDate']
                issueDate = datetime.strptime(issueDateStr, '%Y-%m-%d %H:%M:%S')
                issueDate = timezone.make_aware(issueDate)
                objData['issueDate'] = issueDate

            if 'reissueDate' in objData and objData['reissueDate'] is not None:
                reissueDateStr = objData['reissueDate']
                reissueDate = datetime.strptime(reissueDateStr, '%Y-%m-%d %H:%M:%S')
                reissueDate = timezone.make_aware(reissueDate)
                objData['reissueDate'] = reissueDate

            existingPrescription = modelClass.objects.filter(issueDate=objData['issueDate'], patient = objData['patient']).exists()
            if existingPrescription:
                print(f"Skipping duplicate prescription for patient {objData['patient']} with date issued {objData['issueDate']}")
                continue

            if 'medication' in objData:
                medicationId = objData['medication']
                medication = Medication.objects.get(pk=int(medicationId))
                objData['medication'] = medication

            appointment_id = objData.get('appointment')
            if appointment_id:
                appointment = Appointment.objects.get(pk=int(appointment_id))
                objData['appointment'] = appointment
            else:
                raise ValueError("Appointment ID is missing")


            patient_id = objData.get('patient')
            if patient_id:
                patient_profile = get_user_profile(patient_id)
                if patient_profile:
                    objData['patient'] = patient_profile
                else:
                    raise ValueError(f"Patient with ID {patient_id} not found")
            else:
                raise ValueError("Patient ID is missing")

            if 'doctor' in objData:
                doctorId = objData['doctor']
                if doctorId is not None:
                    doctor_profile = get_user_profile(objData['doctor'])
                    objData['doctor'] = doctor_profile
                else:
                    objData['doctor'] = None

            if 'nurse' in objData:
                nurseId = objData['nurse']
                if nurseId is not None:
                    nurse_profile = get_user_profile(objData['nurse'])
                    objData['nurse'] = nurse_profile
                else:
                    objData['nurse'] = None

            obj = modelClass.objects.create(**objData)
            print(f"{modelClass.__name__} created for user {objData.get('patient', 'Unknown')}")
        except Exception as e:
            print(f"Error creating {modelClass.__name__}:", e)

def populate_template(csvFileName, modelClass):
    reader = open_csv(csvFileName)
    if not reader:
        return

    if not reader.fieldnames:
        print(f"File {csvFileName} is empty")
        return

    for row in reader:
        objData = {}
        for csvFieldName, fieldValue in row.items():
            if fieldValue == 'TRUE' or fieldValue == 'FALSE':
                fieldValue = parse_bool(fieldValue)
            elif fieldValue is not None and isinstance(modelClass._meta.get_field(csvFieldName), models.IntegerField):
                fieldValue = parse_int(fieldValue)

            objData[csvFieldName] = fieldValue

        try:
            if 'dateIssued' in objData:
                dateIssuedStr = objData['dateIssued']
                dateIssued = datetime.strptime(dateIssuedStr, '%Y-%m-%d %H:%M:%S')
                dateIssued = timezone.make_aware(dateIssued)
                objData['dateIssued'] = dateIssued

            existingInvoice = modelClass.objects.filter(dateIssued=objData['dateIssued'], patient = objData['patient']).exists()
            if existingInvoice:
                print(f"Skipping duplicate invoice for patient {objData['patient']} with date issued {objData['dateIssued']}")
                continue

            appointment_id = objData.get('appointment')
            if appointment_id:
                appointment = Appointment.objects.get(pk=int(appointment_id))
                objData['appointment'] = appointment
            else:
                raise ValueError("Appointment ID is missing")


            patient_id = objData.get('patient')
            if patient_id:
                patient_profile = get_user_profile(patient_id)
                if patient_profile:
                    objData['patient'] = patient_profile
                else:
                    raise ValueError(f"Patient with ID {patient_id} not found")
            else:
                raise ValueError("Patient ID is missing")

            obj = modelClass.objects.create(**objData)
            print(f"{modelClass.__name__} created for user {objData.get('patient', 'Unknown')}")

        except Exception as e:
            print(f"Error creating {modelClass.__name__}:", e)
                
def populate_timetables(csvFileName):
    print("Populating timetables...")
    with open(csvFileName, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:

            practitioner_id = row.get('practitioner')

            # Check if the timetable entry already exists
            existingPractitionerEntry = Timetable.objects.filter(practitioner_id=practitioner_id).exists()
            if existingPractitionerEntry:
                print(f"Skipping duplicate timetable entry")
                continue

            practitioner = UserProfile.objects.get(pk=int(practitioner_id))

            commonFields = {
                'practitioner': practitioner,
                'monday': parse_bool(row.get('monday')),
                'tuesday': parse_bool(row.get('tuesday')),
                'wednesday': parse_bool(row.get('wednesday')),
                'thursday': parse_bool(row.get('thursday')),
                'friday': parse_bool(row.get('friday')),
                'saturday':parse_bool(row.get('saturday')),
                'sunday': parse_bool(row.get('sunday')),
            }
            user = Timetable.objects.create(**commonFields)


# Create groups
def create_groups():
    print("Creating groups...")
    group_names = ['doctor_group', 'nurse_group', 'patient_group', 'admin_group']
    groups = [Group.objects.get_or_create(name=name)[0] for name in group_names]

    # Assign users to groups based on their roles
    doctor_profiles = UserProfile.objects.filter(user_type='doctor')
    doctor_users = [profile.user for profile in doctor_profiles]
    nurse_profiles = UserProfile.objects.filter(user_type='nurse')
    nurse_users = [profile.user for profile in nurse_profiles]
    patient_profiles = UserProfile.objects.filter(user_type='patient')
    patient_users = [profile.user for profile in patient_profiles]
    admin_profiles = UserProfile.objects.filter(user_type='admin')
    admin_users = [profile.user for profile in admin_profiles]

    for user in doctor_users:
        user.groups.add(groups[0])
    print("Doctors added to group")
    for user in nurse_users:
        user.groups.add(groups[1])
    print("Nurses added to group")
    for user in patient_users:
        user.groups.add(groups[2])
    print("Patients added to group")
    for user in admin_users:
        user.groups.add(groups[3])
    print("Admins added to group")
if __name__ == '__main__':
    print("Starting to populate the database... ")
    populate_users('data/admins.csv', 'admin', AdminProfile, [])
    populate_users('data/doctors.csv', 'doctor', DoctorProfile, ['specialization', 'isPartTime'])
    populate_users('data/nurses.csv', 'nurse', NurseProfile, [])
    populate_users('data/patients.csv', 'patient', PatientProfile, ['allergies', 'isPrivate'])
    populate_contact('data/address.csv', Address)
    populate_contact('data/contactnumber.csv', ContactNumber)
    populate_services('data/service.csv', Service, 'service', ignore_service= True)
    populate_services('data/doctorservicerate.csv', DoctorServiceRate)
    populate_services('data/nurseservicerate.csv', NurseServiceRate)
    populate_medication('data/medication.csv', Medication, 'name')
    populate_appointment('data/appointment.csv', Appointment)
    populate_prescription('data/prescription.csv', Prescription)
    populate_template('data/invoice.csv', Invoice)
    populate_timetables('timetable.csv')
    create_groups()
    print("Populating complete!")