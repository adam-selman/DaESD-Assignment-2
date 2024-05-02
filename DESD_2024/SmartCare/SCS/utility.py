"""
This file contains utility functions that are used in the SmartCare System
"""

from datetime import datetime
import logging 
import os
import shutil
import csv
from io import StringIO

from django.conf import settings
from .models import Service, DoctorServiceRate, NurseServiceRate, User, \
        UserProfile, Prescription, Appointment, Service, \
        Invoice, Address, PatientProfile
from .db_utility import get_patient_appointments_by_user_id, get_service_rate_by_appointment, get_practitioner_name_by_user_profile_id, get_user_by_user_profile, get_all_appointments_by_patient_profile

logger = logging.getLogger(__name__)

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


def generate_invoice_file_content(invoice_id: int) -> tuple:
    """
    Generates an invoice file and serves it

    Args:
        invoice_id (int): The id of the invoice

    Returns:
        str, str: The content of the invoice file to be written
    """
    file_content, file_name = create_invoice_file(invoice_id)
    
    return file_content, file_name

def generate_patient_forwarding_file_content(patient_profile: PatientProfile) -> tuple:
    """
    Generates an patient forwarding file and serves it

    Args:
        patient_id (int): The id of the patient

    Returns:
        str, str: The content of the invoice file to be written
    """

    # create the file content
    file_content, file_name = create_patient_forwarding_file(patient_profile)
    
    return file_content, file_name


def create_invoice_file(invoice_id: int) -> tuple:
    """
    Creates an invoice file

    Args:
        invoice_id (int): The id of the invoice

    Returns:
        str, str: The file contents of the invoice and the file name
    """

    # invoice info
    invoice = Invoice.objects.get(invoiceID=invoice_id)

    # appointment info
    appointment = Appointment.objects.get(appointmentID=invoice.appointment.appointmentID)

    # service info
    service = Service.objects.get(serviceID=appointment.service.serviceID)
    service_name = service.service.title()
    service_rate = float(get_service_rate_by_appointment(appointment))

    
    invoice_creation_date = invoice.dateIssued
    invoice_creation_date = invoice_creation_date.strftime("%d/%m/%Y")
    duration = invoice.appointment.service.duration 
    amount = round(float(service_rate * duration),2 )
    duration = duration * 15
    duration = f"{duration} minutes"
    tax_amount = round((amount * 0.2), 2)
    pre_tax_amount = amount - tax_amount

    # format as strings to 2dp
    amount = "{:.2f}".format(amount)
    tax_amount = "{:.2f}".format(tax_amount)
    pre_tax_amount = "{:.2f}".format(pre_tax_amount)
    
    if invoice.approved is True:
        payment_status = "Paid"
    elif invoice.status == 0:
        payment_status = "Unpaid"
    elif invoice.status == 1:
        payment_status = "Payment Submitted. Pending Approval"
    
    # patient info
    user_profile = invoice.patient
    patient_user_profile = PatientProfile.objects.get(id=user_profile.id)
    # patient_address = Address.objects.get(user_id=patient_user_profile.user_id) #! FIX FOR ADDRESS
    # address_string = str(patient_address)
    address_string = "123 Fake Street, Fake Town, Fake City, Fake Country, F4K3 123" #! REPLACE WITH ACTUAL ADDRESS
    user = User.objects.get(id=patient_user_profile.user_profile_id)

    # getting files ready
    invoice_template_path = settings.INVOICE_TEMPLATE_PATH
    file_name = f"{user.first_name}_{user.last_name}_invoice_{invoice_id}.txt"

    with open(invoice_template_path, 'r') as file:
        template = file.read()

    invoice_data = {
        'invoice_id': invoice_id,
        'invoice_creation_date': invoice_creation_date,
        'patient_name': f"{user.first_name} {user.last_name}",
        'patient_address': address_string,
        'service_name': service_name,
        'duration': duration,
        'service_rate': service_rate,
        'billing_party': invoice.billingParty,
        'total_amount': amount,
        'tax_amount': tax_amount,
        'pre_tax_amount': pre_tax_amount,
        'payment_status': payment_status,
    }

    filled_template = populate_template(template, invoice_data)

    return filled_template, file_name


def populate_template(template, data) -> str:
    """
    Populates the template with the provided data

    Args:
        template (str): The template to populate
        data (dict): The data to populate the template with

    Returns:
        str: The filled template
    """

    filled_template = template
    for key, value in data.items():
        filled_template = filled_template.replace('{{' + key + '}}', str(value))

    return filled_template

def create_patient_forwarding_file(patient: PatientProfile) -> tuple:
    """
    Creates a patient forwarding file

    Args:
        patient_id (int): The id of the patient

    Returns:
        tuple: The content of the patient forwarding file and the file name
    """
    

    # appointment history
    appointment_string = ""
    past_appointments = get_all_appointments_by_patient_profile(patient)
    if len(past_appointments) < 1:
        past_appointments = None
    else:
        for appointment in past_appointments:
            date = appointment.date.strftime("%d/%m/%Y")
            time = appointment.time.strftime("%H:%M")
            if appointment.doctor_id is not None:
                practitioner = get_practitioner_name_by_user_profile_id(appointment.doctor_id)
            else:
                practitioner = get_practitioner_name_by_user_profile_id(appointment.nurse_id)
            appointment_string += "######################################################\n"
            appointment_string += f"{date} at {time} - {appointment.service.service} with {practitioner}.\n"
            appointment_string += f"Notes: {appointment.notes}\n"
            appointment_string += "######################################################\n"

    #! Format the appointment times for the file

    # Prescription history
    prescription_string = ""
    prescriptions = Prescription.objects.filter(patient=patient.user_profile)
    if len(prescriptions) < 1:
        prescriptions = None
    else:
        for prescription in prescriptions:
            date_prescribed = prescription.issueDate.strftime("%d/%m/%Y")
            if prescription.doctor_id is not None:
                practitioner_name = get_practitioner_name_by_user_profile_id(prescription.doctor_id)
            else:
                practitioner_name = get_practitioner_name_by_user_profile_id(prescription.nurse_id)
            prescription_string += f"{prescription.dosage} dose of {prescription.medication.name}. Prescribed on {date_prescribed} by {practitioner_name}\n"

    # Patient info
    #! GET ADDRESS FROM USER PROFILE
    # patient_address = Address.objects.get(user_id=patient.user_id)
    # address_string = str(patient_address)
    address_string = "123 Fake Street, Fake Town, Fake City, Fake Country, F4K3 123" #! REPLACE WITH ACTUAL ADDRESS
    user_profile = UserProfile.objects.get(id=patient.user_profile_id)
    user = get_user_by_user_profile(user_profile)

    creation_date = datetime.now()
    creation_date = creation_date.strftime("%d/%m/%Y")

    # preparing the file
    patient_forwarding_template_path = settings.PATIENT_FORWARDING_TEMPLATE_PATH
    file_name = f"{user.first_name}_{user.last_name}_medical_information.txt"

    with open(patient_forwarding_template_path, 'r') as file:
        template = file.read()

    patient_forwarding_data = {
        'appointments': appointment_string,
        'prescriptions': prescription_string,
        'patient_name': f"{user.first_name} {user.last_name}",
        'patient_address': address_string,
        "creation_date": creation_date
    }

    filled_template = populate_template(template, patient_forwarding_data)

    return filled_template, file_name

def get_prescriptions_for_practitioner(user):
    if user.groups.filter(name='Doctor').exists():
        print("Prescriptions found for Doctor" + User.username)
        return Prescription.objects.filter(doctor=user)
    elif user.groups.filter(name='Nurse').exists():
        print("Prescriptions found for Nurse" + User.username)
        return Prescription.objects.filter(nurse=user)
    else:
        return None
    
    
def get_appointments_for_practitioner(user):
    if user.groups.filter(name='Doctor').exists():
        print("Appointments found for Doctor" + User.username)
        return Appointment.objects.filter(doctor=user)
    elif user.groups.filter(name='Nurse').exists():
        print("Appointments found for Nurse" + User.username)
        return Appointment.objects.filter(nurse=user)
    else:
        return None
    
def create_report(start_date, end_date):
    appointment_data = create_report_content(start_date, end_date)

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)

    # write the data to the buffer
    csv_writer.writerow(['Start Date', 'End Date', 'Appointments',
                         'Nurse Appointments', 'Doctor Appointments', 'Expected Turnover',
                         'Turnover', 'Missing Turnover', 'Invoices', 'Paid Invoices',
                         'Unpaid Invoices'])
    
    csv_writer.writerow(appointment_data)

    base_file_name = f"report_{start_date}_to_{end_date}.csv"
    file_name = base_file_name
    file_path = f"/code/SmartCare/Reports/{file_name}"

    counter = 1
    while os.path.exists(file_path):
        file_name = f"{base_file_name.split('.csv')[0]}({counter}).csv"  # Append counter to filename
        file_path = f"/code/SmartCare/Reports/{file_name}"
        counter += 1

    with open(file_path, 'w') as file:
        file.write(csv_buffer.getvalue())

    return file_name

def create_report_content(start_date, end_date):
    appointment_list = Appointment.objects.filter(date__range=[start_date, end_date])
    nurse_appointments = Appointment.objects.filter(nurse__isnull=False, date__range=[start_date, end_date])
    invoice_list = Invoice.objects.filter(dateIssued__range=[start_date, end_date])
    appointments = len(appointment_list)
    nurse_appointments = len(nurse_appointments)
    doctor_appointments = appointments - nurse_appointments
    expected_turnover = 0
    turnover = 0
    invoices = len(invoice_list)
    paid_invoices = 0


    for invoice in invoice_list:
        expected_turnover += invoice.amount
        if invoice.status:
            turnover += invoice.amount
            paid_invoices += 1

    unpaid_invoices = invoices - paid_invoices
    missing_turnover = expected_turnover - turnover


    appointment_data = [start_date, end_date, appointments, nurse_appointments,
                        doctor_appointments, expected_turnover, turnover,
                        missing_turnover, invoices, paid_invoices, unpaid_invoices]

    return appointment_data