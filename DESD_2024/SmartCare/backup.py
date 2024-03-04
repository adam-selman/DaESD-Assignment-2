import os
from datetime import datetime
import django
from django.apps import apps
from django.conf import settings
from django.core.serializers import serialize

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')
django.setup()

def backup_database():
    backupDirectoryName = f"backup_{datetime.now().strftime('%Y-%m-%d')}"
    backupDirectoryPath = os.path.join(settings.BASE_DIR, 'backup', backupDirectoryName)

    os.makedirs(backupDirectoryPath, exist_ok=True)

    for model in apps.get_models():
        appLabel = model._meta.app_label
        modelName = model._meta.object_name
        jsonFilePath = os.path.join(backupDirectoryPath, f"{appLabel}_{modelName}.json")

        with open(jsonFilePath, 'w', encoding='utf-8') as jsonFile:
            querySet = model.objects.all()
            serializedData = serialize('json', querySet)
            jsonFile.write(serializedData)

    print(f"Database backup created at {backupDirectoryPath}")

if __name__ == '__main__':
    backup_database()
