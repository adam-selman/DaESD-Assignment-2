"""
This file contains utility functions that are used in the SmartCare System
"""

from datetime import datetime
import logging 

from .models import Service, Invoice, DoctorServiceRate, NurseServiceRate, User, NurseProfile, UserProfile, Appointment

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
