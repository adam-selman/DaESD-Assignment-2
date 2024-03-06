import os
import sys
from datetime import datetime
import django
from django.apps import apps
from django.conf import settings
from django.core.serializers import serialize

projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

def backup_database():
    backupDirectoryName = f"Backup_{datetime.now().strftime('%Y-%m-%d')}"
    backupDirectoryPath = os.path.join(settings.BASE_DIR, 'Backup', backupDirectoryName)

    try:
        os.makedirs(backupDirectoryPath, exist_ok=True)
    except OSError as e:
        print(f"Error creating backup directory: {e}")
        return

    for model in apps.get_models():
        appLabel = model._meta.app_label
        modelName = model._meta.object_name
        jsonFilePath = os.path.join(backupDirectoryPath, f"{appLabel}_{modelName}.json")
        print(f"Creating backup for {modelName}...")

        try:
            with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
                querySet = model.objects.all()
                serializedData = serialize('json', querySet)
                jsonFile.write(serializedData)
                print(f"Backup created for {modelName}")
        except Exception as e:
            print(f"Error creating backup for {modelName}: {e}")

    print(f"Database backup created at {backupDirectoryPath}")

if __name__ == '__main__':
    backup_database()
