
import django 
import os, sys

projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

from django.contrib.auth.models import Group, User

# Create groups
def create_groups():
    group_names = ['doctor_group', 'nurse_group', 'patient_group', 'admin_group']
    groups = [Group.objects.get_or_create(name=name)[0] for name in group_names]

    # Assign users to groups based on their roles
    doctor_users = User.objects.filter(userprofile__user_type='doctor')
    nurse_users = User.objects.filter(userprofile__user_type='nurse')
    patient_users = User.objects.filter(userprofile__user_type='patient')
    admin_users = User.objects.filter(userprofile__user_type='admin')

    for user in doctor_users:
        user.groups.add(groups[0])
        

    for user in nurse_users:
        user.groups.add(groups[1])

    for user in patient_users:
        user.groups.add(groups[2])

    for user in admin_users:
        user.groups.add(groups[3])
if __name__ == '__main__':
    create_groups()