import os
import sys
import json
import django
from django.apps import apps
from django.conf import settings
from django.core.serializers import deserialize
from django.db.utils import IntegrityError

projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

def restore_database():
    while True:
        backupDate = input("Enter the date of the backup to restore (YYYY-MM-DD): ")
        backupDirectoryName = f"backup_{backupDate}"
        backupDirectoryPath = os.path.join(settings.BASE_DIR, 'backup', backupDirectoryName)

        if os.path.exists(backupDirectoryPath):
            break
        else:
            print(f"No backup found for date: {backupDate}")
    
    modelOrder = ['User', 'Group', 'Permission','UserProfile', 'DoctorProfile',
                   'NurseProfile', 'PatientProfile', 'AdminProfile', 'Timetable',
                   'ContactNumber', 'Address', 'Service', 'DoctorServiceRate',
                   'NurseServiceRate', 'Appointment', 'Medication', 'Prescription',
                   'Invoice', 'LogEntry', 'Session', 'ContentType']

    for modelName in modelOrder:
        for root, dir, files in os.walk(backupDirectoryPath):
            for file in files:
                appLabel, fileModelName = file.split('_', 1)
                fileModelName = fileModelName.split('.')[0]
                
                if fileModelName == modelName:
                    print(f"Restoring {modelName}...")
                    jsonFile_path = os.path.join(root, file)
                    with open(jsonFile_path, 'r', encoding='utf-8') as jsonFile:
                        data = json.load(jsonFile)
                        objects = deserialize('json', json.dumps(data))

                    model = apps.get_model(appLabel, fileModelName)
                    if model is not None:
                        for obj in objects:
                            try:
                                obj.save()
                            except IntegrityError as e:
                                print(f"Error restoring {modelName}: {e}")

            print(f"Restored {modelName}")

    print("Database restore completed.")

if __name__ == '__main__':
    restore_database()
