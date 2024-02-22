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

def populate_doctors():
    reader = open_csv('data/doctors.csv')
    if not reader:
        return
    
    for row in reader:
        if not all(row.values()):
            print("Empty cell foind in the row.")
            break

        username = row.get('username')
        password = row.get('password')
        if username:
            if not User.objects.filter(username = username).exists():
                doctor = User.objects.create_user(username = username, 
                                            password = password,
                                            date_joined = timezone.now())
                print(f"Doctor {username} created")
            else:
                print("user with username {username} already exists")
        else:
            print("username not found")

def populate_admins():
    reader = open_csv('data/admins.csv')
    if not reader:
        return
    
    for row in reader:
        admins = User.objects.create_user(username = row['username'], 
                                    password = row['password'],
                                    date_joined = timezone.now())

def populate_nurses():
    reader = open_csv('data/nurses.csv')
    if not reader:
        return
    
    for row in reader:
        nurses = User.objects.create_user(username = row['username'], 
                                    password = row['password'],
                                    date_joined = timezone.now())

def populate_patients():
    reader = open_csv('data/patients.csv')
    if not reader:
        return
    
    for row in reader:
        patients = User.objects.create_user(username = row['username'], 
                                    password = row['password'],
                                    date_joined = timezone.now())      


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
    #populate_admins()
    #populate_nurses()
    #spopulate_patients()
    print("Populating complete!")