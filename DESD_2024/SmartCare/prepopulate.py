import os
import csv
import django
from django.utils import timezone
from django.db.models import ObjectDoesNotExist

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from SCS.models import *

def parse_bool(value):
    return value.lower() == 'true'

def open_csv(file):
    try:
        file = open(file, 'r')
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

        specificFields = {field: row.get(field) for field in additionalFields}
        if additionalFields:
            for field in additionalFields:
                value = row.get(field)
                if value in {'TRUE', 'FALSE'}:
                    specificFields[field] = parse_bool(value)
                else:
                    specificFields[field] = value

        user = User.objects.create_user(**commonFields)
        
        userProfile = UserProfile.objects.create(user=user, user_type=userType)
        
        specificProfile = profileClass.objects.create(user_profile=userProfile, **specificFields)
        
        print(f"{userType} {row['first_name']} {row['last_name']} created")

def populate_services(csvFileName, modelClass, columnToPrint = None, ignore_service = False):
    with open(csvFileName, 'r') as file:
        reader = csv.DictReader(file)

        csvFieldName = reader.fieldnames

        if not csvFieldName:
            print(f"File {csvFileName} is empty")
            return
        
        fieldMapping = {csvFieldName: csvFieldName for csvFieldName in csvFieldName}

        for row in reader:
            objData = {}
            for csvFieldName, djangoFieldName in fieldMapping.items():
                objData[djangoFieldName] = row[csvFieldName]

            if not ignore_service and 'service' in objData:
                serviceId = objData['service']
                service = Service.objects.get(pk = int(serviceId))

                existingEntry = modelClass.objects.filter(service_id = service).first()
                if existingEntry:
                    print(f"{modelClass.__name__} for {service.service} already exists, skipping.")
                    continue

                objData['service'] = service

            obj = modelClass.objects.create(**objData)

            if columnToPrint is not None:
                if columnToPrint and columnToPrint in row:
                    valueToPrint = row.get(columnToPrint)
                    print(f"{modelClass.__name__} {valueToPrint} created")
            else:
                print(f"{modelClass.__name__} created")

def populate_contact(csvFileName, modelClass):
    with open(csvFileName, 'r') as file:
        reader = csv.DictReader(file)

        csvFieldName = reader.fieldnames

        if not csvFieldName:
            print(f"File {csvFileName} is empty")
            return

        fieldMapping = {csvFieldName: csvFieldName for csvFieldName in csvFieldName}

        for row in reader:
            objData = {}
            for csvFieldName, djangoFieldName in fieldMapping.items():
                objData[djangoFieldName] = row[csvFieldName]

            if 'user' in objData:
                userId = objData['user']
                userProfile = UserProfile.objects.get(pk = int(userId))
                userName =  userProfile.user.username

                objData['user'] = userProfile

            obj = modelClass.objects.create(**objData)

            
            print(f"{modelClass.__name__} created for user {userName}")


if __name__ == '__main__':
    print("Starting to populate the database... ")
    populate_users('data/doctors.csv', 'doctor', DoctorProfile, ['specialization', 'isPartTime'])
    populate_users('data/admins.csv', 'admin', AdminProfile, [])
    populate_users('data/nurses.csv', 'nurse', NurseProfile, [])
    populate_users('data/patients.csv', 'patient', PatientProfile, ['age', 'allergies', 'isPrivate'])
    populate_services('data/service.csv', Service, 'service', ignore_service= True)
    populate_services('data/doctorservicerate.csv', DoctorServiceRate)
    populate_services('data/nurseservicerate.csv', NurseServiceRate)
    populate_contact('data/contactinfo.csv', ContactNumber)
    populate_contact('data/address.csv', Address)
    print("Populating complete!")