from datetime import datetime
import logging 

from .models import Service, Invoice, DoctorServiceRate, NurseServiceRate, User, NurseProfile, UserProfile, Appointment

def get_service_by_appointment_id(appointment_id: int) -> Service:
    """
    Returns the service of an appointment

    Args:
        appointment_id (int): The id of the appointment

    Returns:
        Service: The service of the appointment
    """
    appointment = Appointment.objects.get(appointmentID=appointment_id)
    return appointment.service