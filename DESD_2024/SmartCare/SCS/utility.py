"""
This file contains utility functions that are used in the SmartCare System
"""

from datetime import datetime
import logging 
import os
import shutil

from django.conf import settings

from .models import Service, Invoice, DoctorServiceRate, NurseServiceRate, User, NurseProfile, UserProfile, Appointment, Address

logger = logging.getLogger(__name__)

class BILLABLE_PARTIES:
    """
    Enum for the billing parties
    """
    NHS = 'NHS',
    INSURANCE = 'Insurance'
    PRIVATE = 'Private'

    @property
    def valid_choices(self):
        return [self.NHS, self.INSURANCE, self.PRIVATE]
    
    def validate(self, party: str) -> bool:
        """
        Validates the billing party

        Args:
            party (str): The given billing party string to validate

        Returns:
            bool: Whether the billing party is valid
        """
        if party not in self.valid_choices:
            return False
        return True

def parse_times_for_view(times: list) -> list:
    """
    Parses the times for the view

    Args:
        times (list): The list of times

    Returns:
        list: The list of times to pass to the view
    """
    parsed_times = []
    for time in times:
        parsed_times.append(time.strftime("%H:%M"))
    return parsed_times

def convert_to_datetimes(appointment_times) -> list:
    """
    Converts a list of strings to a list of datetime objects

    Args:
        appointment_times (list[str]): A list of strings representing times

    Returns:
        list: A list of datetime objects
    """

    formatted_times = []
    for time_str in appointment_times:
        formatted_time = datetime.strptime(time_str, "%H:%M:%S").time()
        formatted_times.append(formatted_time)
    return formatted_times

APPOINTMENT_TIMES = convert_to_datetimes(["09:00:00", "09:15:00", "09:30:00", "09:45:00", "10:00:00", \
                               "10:15:00", "10:30:00", "10:45:00", "11:00:00", "11:15:00", \
                               "11:30:00", "11:45:00", "12:00:00", "12:15:00", "12:30:00", \
                               "12:45:00", "13:00:00", "13:15:00", "13:30:00", "13:45:00", \
                               "14:00:00", "14:15:00", "14:30:00", "14:45:00", "15:00:00", \
                               "15:15:00", "15:30:00", "15:45:00", "16:00:00", "16:15:00", \
                               "16:30:00", "16:45:00"])

def get_service_rate_by_appointment(appointment: Appointment) -> float:
    """
    Gets the rate of a service

    Args:
        appointment_id (Appointment): The appointment object

    Returns:
        float: The rate of the service
    """
    service_id = appointment.service_id
    service = Service.objects.get(serviceID=service_id)

    doctor = False
    nurse = False

    if appointment.doctor_id is not None:
        doctor = True
    elif appointment.nurse_id is not None:
        nurse = True
    
    if doctor:
        doctor_service_rate_object = DoctorServiceRate.objects.get(service=service_id) 
        service_rate = doctor_service_rate_object.rate
    else:
        nurse_service_rate_object = NurseServiceRate.objects.get(service=service_id)
        service_rate = nurse_service_rate_object.rate
        
    return service_rate


def calculate_appointment_cost(appointment_id: int) -> float:
    """
    Calculates the cost of an appointment

    Args:
        service_id (int): The id of the service

    Returns:
        float: The cost of the appointment
    """
    appointment = Appointment.objects.get(appointmentID=appointment_id)
    service_id = appointment.service_id
    service = Service.objects.get(serviceID=service_id)
    service_rate = get_service_rate_by_appointment(appointment)
    
    cost = service_rate * service.duration
    
    return cost


def generate_invoice_file(invoice_id: int) -> str:
    """
    Generates an invoice file and serves it

    Args:
        invoice_id (int): The id of the invoice

    Returns:
        str: The path to the invoice file
    """
    invoice = Invoice.objects.get(invoiceID=invoice_id)
    file_path = create_invoice_file(invoice_id)
    
    return file_path


def create_invoice_file(invoice_id: int) -> str:
    """
    Creates an invoice file

    Args:
        invoice_id (int): The id of the invoice

    Returns:
        str: The path to the invoice file
    """
    invoice = Invoice.objects.get(invoiceID=invoice_id)
    invoice_creation_date = invoice.date
    duration = invoice.appointment.duration_id
    amount = invoice.amount
    tax_amount = amount * 0.2
    current_date = datetime.now()
    appointment = Appointment.objects.get(appointmentID=invoice.appointment).first()
    service = Service.objects.get(serviceID=appointment.service).first()
    service_name = service.service.title()
    service_rate = get_service_rate_by_appointment(appointment)
    patient = invoice.patient
    patient_user_profile = UserProfile.objects.get(user_id=patient.user_id).first()
    patient_address = Address.objects.get(user_id=patient_user_profile.user_id).first()
    address_string = str(patient_address)
    user = User.objects.get(user_id=patient.user_id)

    # getting files ready
    static_dir = settings.STATIC_ROOT
    invoice_template_path = os.path.join(static_dir, settings.INVOICE_TEMPLATE_FILENAME)
    temp_file_directory = settings.TEMP_FILE_DIRECTORY
    destination_file =  os.path.join(temp_file_directory, f"{user.first_name}_{user.last_name}_invoice_{invoice_id}.txt")

    # Check if the source file exists
    if os.path.exists(invoice_template_path):
        # Copy the file
        shutil.copy(invoice_template_path, destination_file)
        logger.info("Invoice copied successfully!")
    else:
        logger.info("Source file does not exist.")

    with open(destination_file, 'r') as file:
        template = file.read()

    invoice_data = {
        'invoice_id': invoice_id,
        'invoice_creation_date': invoice_creation_date,
        'patient_name': f"{user.first_name} {user.last_name}",
        'patient_address': address_string,
        'service_name': service_name,
        'duration': duration,
        'service_rate': service_rate,
        'billing_party': invoice.billing_party,
        'total_amount': amount,
        'tax_amount': tax_amount,
        'pre_tax_amount': amount - tax_amount,
    }

    filled_template = populate_invoice(template, invoice_data)

    with open(destination_file, 'w') as file:
        file.write(filled_template)

    return destination_file


def populate_invoice(template, invoice_data):

    filled_template = template
    for key, value in invoice_data.items():
        filled_template = filled_template.replace('{{' + key + '}}', str(value))

    return filled_template