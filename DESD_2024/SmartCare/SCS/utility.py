"""
This file contains utility functions that are used in the SmartCare System
"""

from datetime import datetime
import logging 

from .db_utility import get_service_by_appointment_id
from .models import Service, Invoice, DoctorServiceRate, NurseServiceRate, User, NurseProfile, UserProfile, Appointment

logger = logging.getLogger(__name__)

def get_medical_services() -> list:
    """
    Returns a list of available services

    Returns:
        list: Returns a list of services to pass to a view as context
    """

    service_options = []

    services = Service.objects.all()

    for service in services:
        service_options.append([service.serviceID, service.service, service.duration])    

    return service_options

def get_invoice_information_by_user_id(user_id: int) -> list:
    """
    Returns the invoices for a user

    Args:
        user_id (int): The user id

    Returns:
        list: The invoices for the user
    """
    invoices = Invoice.objects.filter(patient_id=user_id).all()
    invoice_info = []
    for invoice in invoices:
        service = get_service_by_appointment_id(invoice.appointment_id)
        service_name = service.service
        amount = invoice.amount
        issue_date = invoice.dateIssued.strftime("%d-%m-%Y")
        invoice_info.append([service_name, amount, issue_date])
    return invoice_info

def get_user_profile_by_user_id(user_id: int) -> int:
    """
    Returns the user profile 
    Args:
        user_id (int): The user id 

    Returns:
        UserProfile: The user profile of the user
    """
    user_profile = UserProfile.objects.get(user_id=user_id)
    return user_profile


def check_practitioner_service(service_id: int, doctor=False, nurse=False) -> bool:
    """
    Checks if a practitioner provides a given service

    Args:
        practitioner (_type_): _description_
        service (_type_): _description_

    Returns:
        bool: Returns True if the practitioner provides the service, False otherwise
    """
    can_perform = False
    if doctor is False and nurse is False:
        raise ValueError("Doctor and nurse cannot both be False")
    
    if doctor:
        service = DoctorServiceRate.objects.filter(service=service_id).all()
        if len(service) > 0:
            can_perform = True
        else:
            can_perform = False

    if nurse:
        service = NurseServiceRate.objects.filter(service=service_id).all()
        if len(service) > 0:
            can_perform = True
        else:
            can_perform = False

    return can_perform


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

    doctor = False
    nurse = False

    if appointment.doctor_id is not None:
        doctor = True
    elif appointment.nurse_id is not None:
        nurse = True
    else:
        raise ValueError("Appointment must have a doctor or a nurse")
    
    if doctor:
        doctor_service_rate_object = DoctorServiceRate.objects.get(service=service_id) 
        service_rate = doctor_service_rate_object.rate * service.duration
    else:
        nurse_service_rate_object = NurseServiceRate.objects.get(service=service_id)
        service_rate = nurse_service_rate_object.rate * service.duration
        
    
    return service_rate
