import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from SCS.models import User, Profile, ContactInfo, Address, Appointment, Invoice, Service, AppointmentService, DoctorServiceRate

# To add dummy data, run the following command in the terminal:
# docker compose run django sh -c "cd/code/SmartCare/ && python dummy.py"

def populate_dummy_data():
    # Create user instances
    user1 = User.objects.create_user(username = 'user1', password = 'password1',
                email = 'user1@email.com', first_name = 'User', last_name = 'One', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user2 = User.objects.create_user(username = 'user2', password = 'password2', 
                email = 'user2@email.com', first_name = 'User', last_name = 'Two', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user3 = User.objects.create_user(username = 'user3', password = 'password3', 
                email = 'user3@email.com', first_name = 'User', last_name = 'Three', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user4 = User.objects.create_user(username = 'user4', password = 'password4', 
                email = 'user4@email.com', first_name = 'User', last_name = 'Four', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user5 = User.objects.create_user(username = 'user5', password = 'password5', 
                email = 'user5@email.com', first_name = 'User', last_name = 'Five', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user6 = User.objects.create_user(username = 'user6', password = 'password6', 
                email = 'user6@email.com', first_name = 'User', last_name = 'Six', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user7 = User.objects.create_user(username = 'user7', password = 'password7', 
                email = 'user7@email.com', first_name = 'User', last_name = 'Seven', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user8 = User.objects.create_user(username = 'user8', password = 'password8', 
                email = 'user8@email.com', first_name = 'User', last_name = 'Eight', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')
    user9 = User.objects.create_user(username = 'user9', password = 'password9', 
                email = 'user9@email.com', first_name = 'User', last_name = 'Nine', 
                is_active = True, date_joined = timezone.now(), gender = 'Male', 
                allergies = False, dob = '1990-01-01')

    profile1 = Profile.objects.create(user = user1, isPatient = True)
    profile2 = Profile.objects.create(user = user2, isDoctor = True, 
                                      isPartTime = True)
    profile3 = Profile.objects.create(user = user3, isDoctor = True, 
                                      isPartTime = False)
    profile4 = Profile.objects.create(user = user4, isNurse = True)
    profile5 = Profile.objects.create(user = user5, isAdmin = True)
    profile6 = Profile.objects.create(user = user6, isNHSTrust = True)
    profile7 = Profile.objects.create(user = user7, isPatient = True, 
                                      isDoctor = True, isPartTime = True)
    profile8 = Profile.objects.create(user = user8, isPatient = True, 
                                      isDoctor = True, isPartTime = False)
    profile9 = Profile.objects.create(user = user9, isPatient = True, 
                                      isNurse = True)

if __name__ == '__main__':
    print('Populating dummy data...')
    populate_dummy_data()
    print('Populating complete.')