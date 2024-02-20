import os
import csv
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from SCS.models import *

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
                                        allergies = row['allergies'],
                                        is_active = row['active'], 
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
                                            isPatient = row['patient'],
                                            isDoctor = row['doctor'],
                                            isPartTime = row['part time'],
                                            isNurse = row['nurse'],
                                            isAdmin = row['admin'],
                                            isNHSTrust = row['trust'])

if __name__ == '__main__':
    print("Starting to populate the database... ")
    populate_users()
    populate_profiles()
    print("Populating complete!")