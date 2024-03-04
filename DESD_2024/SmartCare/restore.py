import os
import json
import django
from django.apps import apps
from django.conf import settings
from django.core.serializers import deserialize

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

def restore_database():
    backupDate = input("Enter the date of the backup to restore (YYYY-MM-DD): ")
    
    backupDirectoryName = f"backup_{backupDate}"
    backupDirectoryPath = os.path.join(settings.BASE_DIR, 'backup', backupDirectoryName)

    if not os.path.exists(backupDirectoryPath):
        print(f"No backup found for date: {backupDate}")
        return
    
    appLabel = input("Enter the app label to restore (e.g. SCS): ")
    modelName = input("Enter the model name to restore (e.g. UserProfile): ")
    fileName = f"{appLabel}_{modelName}.json"
    filePath = os.path.join(backupDirectoryPath, fileName)

    if not os.path.exists(filePath):
        print(f"No backup found for model '{modelName}' and app '{appLabel}'")
        return

    with open(filePath, 'r', encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        objects = deserialize('json', json.dumps(data))

    model = apps.get_model(appLabel, modelName)
    if model is not None:
        for obj in objects:
            obj.save()

    print("Database restore completed.")

if __name__ == '__main__':
    restore_database()
