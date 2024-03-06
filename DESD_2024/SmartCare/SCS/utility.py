"""
This file contains utility functions that are used in the SmartCare System
"""
import logging 

from .models import Service, DoctorServiceRate, NurseServiceRate

logger = logging.getLogger(__name__)

def get_medical_services() -> list:
    """
    Returns a list of available services

    Args:
        request (_type_): _description_

    Returns:
        list: Returns a list of services to pass to a view as context
    """

    service_options = []

    services = Service.objects.all()

    for service in services:
        service_options.append([service.serviceID, service.service, service.duration])    

    return service_options

def check_practicioner_service(service_id: int, doctor=False, nurse=False) -> bool:
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