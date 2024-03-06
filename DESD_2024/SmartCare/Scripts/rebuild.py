import django
from django.core.management import execute_from_command_line
from django.db import connection
from django.db.utils import OperationalError
import os
import sys

projectDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(projectDirectory)

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

def confirm_action(prompt):
    while True:
        response = input(prompt).lower()
        if response == 'y':
            return True
        elif response == 'n':
            print('Action canceled.')
            sys.exit(0)
        else:
            print('Invalid input. Please enter y or n.')

def confirm_rebuild():
    if not confirm_action('This will drop and recreate the database. Are you sure you want to continue? (y/n): '):
        return False
    if not confirm_action('Are you absolutely certain? (y/n): '):
        return False
    return True

def delete_migration_files():
    migrationsDirectory = os.path.join(projectDirectory, 'SCS', 'migrations')
    if os.path.exists(migrationsDirectory):
        for fileName in os.listdir(migrationsDirectory):
            if fileName.endswith('.py') and fileName != '__init__.py':
                os.remove(os.path.join(migrationsDirectory, fileName))

# Main function to run the script
def main():
    # Prompt for confirmation
    if confirm_rebuild():
        print("Rebuilding database...")
    else:
        print("Rebuild canceled.")

    # Rebuild the database
    rebuild_database()
    print('Database rebuilt.')

    # Clear previous migrations
    print('Deleting migration files...')
    delete_migration_files()
    print('Migration files deleted.')
    
    # Run the migrations
    print('Running migrations...')
    run_migrations()
    print('Migrations complete.')

if __name__ == '__main__':
    main()