import os
import csv
import django
from django.utils import timezone

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

def populate_users():
    reader = open_csv('data/users.csv')
    if not reader:
        return
    
    for row in reader:
        user = User.objects.create_user(username = row['username'], 
                                    password = row['password'], 
                                    email = row['email'],
                                    first_name = row['firstname'], 
                                    last_name = row['lastname'],
                                    dob = row['date of birth'],
                                    gender = row['gender'],
                                    allergies = parse_bool(row['allergies']),
                                    is_active = parse_bool(row['active']), 
                                    date_joined = timezone.now())

def populate_profiles():
    reader = open_csv('data/profiles.csv')
    if not reader:
        return
    
    for row in reader:
        user_id = int(row['user'])
        user = get_user_by_id(user_id)
        if user:
            profile = Profile.objects.create(user = user,
                                            isPatient = parse_bool(row['patient']),
                                            isDoctor = parse_bool(row['doctor']),
                                            isPartTime = parse_bool(row['part time']),
                                            isNurse = parse_bool(row['nurse']),
                                            isAdmin = parse_bool(row['admin']),
                                            isNHSTrust = parse_bool(row['trust']))
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
    populate_users()
    populate_profiles()
    print("Populating complete!")