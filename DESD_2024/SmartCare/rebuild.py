import django
from django.core.management import execute_from_command_line
from django.db import connection
from django.db.utils import OperationalError
import os
import sys

# Set the Django settings module for the script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartCare.settings')

# Drop and recreate the database
def rebuild_database():
    with connection.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS SCdb')
        cursor.execute('CREATE DATABASE SCdb')

# Run migrations to ensure the schema is up to date
def run_migrations():
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])

# Main function to run the script
def main():
    # Prompt for confirmation
    confirm = input('This will drop and recreate the database. Are you sure you want to continue? (y/n): ')
    if confirm.lower() != 'y':
        print('Rebuild cancelled.')
        sys.exit(0)

    # Rebuild the database
    print('Rebuilding database...')
    rebuild_database()
    print('Database rebuilt.')
    # Run the migrations
    print('Running migrations...')
    run_migrations()
    print('Migrations complete.')

if __name__ == '__main__':
    main()