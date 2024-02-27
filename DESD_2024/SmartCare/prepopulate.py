import os
import csv
import django
from django.utils import timezone
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from SCS.models import *

def parse_bool(value):
    return value.lower() == 'true'

def open_csv(file):
    try:
        file = open(file, 'r')
        #reader = csv.DictReader(file)
        #cleaned_rows = [row for row in reader if all(row.values())]
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
    

def populate_doctors():
    reader = open_csv('data/doctors.csv')
    if not reader:
        return
    
    for row in reader:
        username = row.get('username')
        if check_duplicate_user(username):
            print(f"User with username {username} already exists, skipping.")
            continue
        password = row.get('password')
        firstName = row.get('first name')
        lastName = row.get('last name')
        email = row.get('email')
        specialization = row.get('specialization')
        isPartTime = parse_bool(row.get('part time'))
        user = User.objects.create_user(username=username, 
                                        password = password, 
                                        first_name = firstName, 
                                        last_name = lastName, 
                                        email = email, 
                                        date_joined = timezone.now())
        userProfile = UserProfile.objects.create(user = user, 
                                                 user_type = 'doctor')
        doctor = DoctorProfile.objects.create(user_profile = userProfile, 
                                              specialization = specialization, 
                                              isPartTime = isPartTime)
        print(f"Doctor {username} created")

def populate_admins():
    reader = open_csv('data/admins.csv')
    if not reader:
        return
    
    for row in reader:
        username = row.get('username')
        if check_duplicate_user(username):
            print(f"User with username {username} already exists, skipping.")
            continue
        password = row.get('password')
        firstName = row.get('first name')
        lastName = row.get('last name')
        email = row.get('email')
        user = User.objects.create_user(username=username, 
                                        password = password, 
                                        first_name = firstName, 
                                        last_name = lastName, 
                                        email = email, 
                                        date_joined = timezone.now())
        userProfile = UserProfile.objects.create(user = user, 
                                                 user_type = 'admin')
        admin = AdminProfile.objects.create(user_profile = userProfile)
        print(f"Admin {username} created")

def populate_patients():
    reader = open_csv('data/patients.csv')
    if not reader:
        return
    
    for row in reader:
        username = row.get('username')
        if check_duplicate_user(username):
            print(f"User with username {username} already exists, skipping.")
            continue
        password = row.get('password')
        firstName = row.get('first name')
        lastName = row.get('last name')
        email = row.get('email')
        age = row.get('age')
        private = parse_bool(row.get('private patient'))
        user = User.objects.create_user(username=username, 
                                        password = password, 
                                        last_name = lastName, 
                                        email = email, 
                                        date_joined = timezone.now())
        userProfile = UserProfile.objects.create(user = user, 
                                                 user_type = 'patient')
        patient = PatientProfile.objects.create(user_profile = userProfile, 
                                                age = age, 
                                                isPrivate = private)
        print(f"Patient {username} created")

def populate_nurses():
    reader = open_csv('data/nurses.csv')
    if not reader:
        return
    
    for row in reader:
        username = row.get('username')
        if check_duplicate_user(username):
            print(f"User with username {username} already exists, skipping.")
            continue
        password = row.get('password')
        firstName = row.get('first name')
        lastName = row.get('last name')
        email = row.get('email')
        user = User.objects.create_user(username=username, password = password, first_name = firstName, last_name = lastName, email = email, date_joined = timezone.now())
        userProfile = UserProfile.objects.create(user = user, user_type = 'nurse')
        nurse = NurseProfile.objects.create(user_profile = userProfile)
        print(f"Nurse {username} created")

'''
def populate_contact_info():
    with open('data/contact_info.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = int(row['user'])

            try:
                user = User.objects.get(userID = user_id)
            except User.DoesNotExist:
                print(f"User with ID {user_id} does not exist")
                return
            
            contactInfo = ContactInfo.objects.create(contactType = row['contact type'],
                                                     contactValue = row['contact value'],
                                                    description = row['description'],
                                                    user = user)
            
def populate_addresses():
    with open('data/addresses.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = int(row['user'])

            try:
                user = User.objects.get(userID = user_id)
            except User.DoesNotExist:
                print(f"User with ID {user_id} does not exist")
                return
            
            address = Address.objects.create(addressID = int(row['addressID']),
                                            number = int(row['number']),
                                            buildingName = row['building name'],
                                            streetName = row['street name'],
                                            city = row['city'],
                                            county = row['county'],
                                            postcode = row['postcode'],
                                            country = row['country'],
                                            description = row['description'],
                                            user = user)

def populate_appointments():
    with open('data/appointments.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
 '''       

if __name__ == '__main__':
    print("Starting to populate the database... ")
    populate_doctors()
    populate_admins()
    populate_nurses()
    populate_patients()
    print("Populating complete!")