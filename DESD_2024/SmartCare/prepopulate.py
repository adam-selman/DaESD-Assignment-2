import os
import csv
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from SCS.models import *

def parse_bool(value):
    return value.lower() == 'true'

def populate_users():
    with open('data/users.csv', 'r') as file:
        reader = csv.DictReader(file)
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
    with open('data/profiles.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            user_id = int(row['user'])

            try:
                user = User.objects.get(userID = user_id)
            except User.DoesNotExist:
                print(f"User with ID {user_id} does not exist")
                return
            
            profile = Profile.objects.create(user = user,
                                            isPatient = parse_bool(row['patient']),
                                            isDoctor = parse_bool(row['doctor']),
                                            isPartTime = parse_bool(row['part time']),
                                            isNurse = parse_bool(row['nurse']),
                                            isAdmin = parse_bool(row['admin']),
                                            isNHSTrust = parse_bool(row['trust']))

if __name__ == '__main__':
    print("Starting to populate the database... ")
    populate_users()
    populate_profiles()
    print("Populating complete!")