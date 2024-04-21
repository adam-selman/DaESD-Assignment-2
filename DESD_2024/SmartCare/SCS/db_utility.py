from datetime import datetime
import logging 
import copy 

from .models import Service, Invoice, DoctorServiceRate, Timetable, NurseServiceRate, User, DoctorProfile, NurseProfile, UserProfile, Appointment, PatientProfile
from .utility import BILLABLE_PARTIES, calculate_appointment_cost, APPOINTMENT_TIMES


logger = logging.getLogger(__name__)

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

def create_invoice_for_appointment(appointment_id: int, billing_party: str) -> None:
    """
    Creates an invoice

    Args:
        appointment_id (int): The id of the appointment

    Returns:
        None
    """

    if billing_party not in BILLABLE_PARTIES.valid_choices:
        raise ValueError("Billing party must be NHS, Insurance or Private.")

    amount = calculate_appointment_cost(appointment_id)
    appointment = Appointment.objects.get(appointmentID=appointment_id)

    previous_invoice = Invoice.objects.filter(appointment_id=appointment_id).first()

    # check if invoice exists for given appointment
    if previous_invoice is not None:
        logger.info(f"An invoice for appointment {appointment_id} already exists")
        raise ValueError("An invoice for this appointment already exists")
        return
    else:
        invoice = Invoice(amount=amount,
                        status=False,
                        dateIssued=datetime.now(),
                        appointment_id=appointment_id,
                        patient_id=appointment.patient_id,
                        billingParty=billing_party)
        invoice.save()

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
        service_name = service.service.title()
        amount = invoice.amount
        issue_date = invoice.dateIssued.strftime("%d-%m-%Y")
        invoice_info.append([service_name, amount, issue_date, invoice.invoiceID, invoice.status])
    return invoice_info

def get_all_invoice_information() -> list:
    """
    Returns a list of all invoices

    Returns:
        list: A list of all invoices
    """
    invoices = Invoice.objects.all()
    invoice_info = []
    for invoice in invoices:
        service = get_service_by_appointment_id(invoice.appointment_id)
        service_name = service.service.title()
        amount = invoice.amount
        issue_date = invoice.dateIssued.strftime("%d-%m-%Y")
        invoice_info.append([service_name, amount, issue_date, invoice.invoiceID, invoice.status])
    return invoice_info

def get_patient_appointments_by_user_id(user_id: int, future=False, past=False) -> list:
    """
    Returns the appointments for a patient

    Args:
        user_id (int): The user id

    Returns:
        list: The appointments for the patient
    """
    user_profile = UserProfile.objects.get(user_id=user_id)
    patient_profile = PatientProfile.objects.get(user_profile_id=user_profile.id)
    appointments = Appointment.objects.filter(patient_id=patient_profile.id).all()
    appointment_info = []
    for appointment in appointments:
        service = get_service_by_appointment_id(appointment.appointmentID)
        service_name = service.service.title()

        if future:
            if appointment.date >= datetime.now().date():
                appointment_info.append([service_name, appointment.date, appointment.time, appointment.appointmentID])
        elif past:
            if appointment.date < datetime.now().date():
                appointment_info.append([service_name, appointment.date, appointment.time, appointment.appointmentID])
        else:
            appointment_info.append([service_name, appointment.date, appointment.time, appointment.appointmentID])
    return appointment_info

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

def get_patient_profile_by_user_id(user_id: int) -> int:
    """
    Returns the patient profile 
    Args:
        user_id (int): The user id 

    Returns:
        PatientProfile: The patient profile of the user
    """
    user_profile = UserProfile.objects.get(user_id=user_id)
    patient_profile = PatientProfile.objects.get(user_profile_id=user_profile.id)
    return patient_profile

def get_practitioners_by_day_and_service(service, day_of_week) -> dict:

    doctors = []
    nurses = []

    doctor_can_perform = check_practitioner_service(service, doctor=True)
    nurse_can_perform = check_practitioner_service(service, nurse=True)

    if doctor_can_perform:
        all_doctors = DoctorProfile.objects.all()

        for doctor in all_doctors:
            doctor_user_profile = UserProfile.objects.filter(id=doctor.user_profile_id).first()
            doctor_user_info = User.objects.filter(id=doctor_user_profile.user_id).first()
            doctor_timetable = Timetable.objects.filter(practitioner_id=doctor.user_profile_id).first()
            doctor_available = False
            if day_of_week == "monday":
                doctor_available = doctor_timetable.monday
            elif day_of_week == "tuesday":
                doctor_available = doctor_timetable.tuesday
            elif day_of_week == "wednesday":
                doctor_available = doctor_timetable.wednesday
            elif day_of_week == "thursday":
                doctor_available = doctor_timetable.thursday
            elif day_of_week == "friday":
                doctor_available = doctor_timetable.friday
            elif day_of_week == "saturday":
                doctor_available = doctor_timetable.saturday
            elif day_of_week == "sunday":
                doctor_available = doctor_timetable.sunday
            
            if doctor_available:
                doctors.append((doctor_user_info.first_name + " " + doctor_user_info.last_name, doctor_user_info.id))

    if nurse_can_perform:
        all_nurses = NurseProfile.objects.all()

        for nurse in all_nurses:
            nurse_user_profile = UserProfile.objects.filter(id=nurse.user_profile_id).first()
            nurse_user_info = User.objects.filter(id=nurse_user_profile.user_id).first()

            nurse_timetable = Timetable.objects.filter(practitioner_id=nurse.user_profile_id).first()
            
            nurse_available = False
            if day_of_week == "monday":
                nurse_available = nurse_timetable.monday
            elif day_of_week == "tuesday":
                nurse_available = nurse_timetable.tuesday
            elif day_of_week == "wednesday":
                nurse_available = nurse_timetable.wednesday
            elif day_of_week == "thursday":
                nurse_available = nurse_timetable.thursday
            elif day_of_week == "friday":
                nurse_available = nurse_timetable.friday
            elif day_of_week == "saturday":
                nurse_available = nurse_timetable.saturday
            elif day_of_week == "sunday":
                nurse_available = nurse_timetable.sunday
            
            if nurse_available:
                nurses.append((nurse_user_info.first_name + " " + nurse_user_info.last_name, nurse_user_info.id))
    practitioners = {"doctors": doctors,
                    "nurses": nurses}

    return practitioners


def get_time_slots_by_day_and_practitioner(practitioner_id: int, booking_date) -> list:
    """
    Returns the available time slots for a practitioner on a given day

    Args:
        practitioner (int): The id of the practitioner
        booking_date (datetime): The date of the booking

    Returns:
        list: _description_
    """

    current_date = datetime.now().strftime("%Y-%m-%d")
    booking_date = booking_date.strftime("%Y-%m-%d")
    current_time = datetime.now().time()

    practitioner_user_profile = get_user_profile_by_user_id(practitioner_id)

    # Get the appointments for the practitioner on the given day
    if practitioner_user_profile.user_type == "doctor":
        booked_appointments = Appointment.objects.filter(doctor_id=practitioner_user_profile, date=booking_date).all()

    elif practitioner_user_profile.user_type == "nurse":
        booked_appointments = Appointment.objects.filter(nurse_id=practitioner_user_profile, date=booking_date).all()

    booked_times = []
    # Get the booked times
    for appointment in booked_appointments:
        booked_times.append([appointment.time, appointment.service.duration])
    
    
    available_times = copy.deepcopy(APPOINTMENT_TIMES)

    # Remove booked times from available times
    for time, duration in booked_times:
        if time in available_times:
            # Remove the time and the following n times based on the duration
            index = available_times.index(time)
            appointment_segments = available_times[index:index + duration]
            for time in appointment_segments:
                available_times.remove(time)

    if booking_date == current_date:
        # removing invalid times
        times_to_remove = []
        for time in available_times:
            # removing times before now
            if time < current_time:
                times_to_remove.append(time)

        for time in times_to_remove:
            available_times.remove(time)

    return available_times

def make_patient_appointment_booking(patient, booking_date, service_id, practitioner, time, reason) -> bool:
    """
    Books an appointment for a patient

    Args:
        patient_id (int): The id of the patient
        practitioner_id (int): The id of the practitioner
        service_id (int): The id of the service
        appointment_time (datetime): The time of the appointment

    Returns:
        dict: A dict containing the success status of the booking and the error message if it failed
    """
    
    if booking_date is None or service_id is None or practitioner is None or time is None or reason is None:
        data = {'success': 'false', 'error': 'Invalid form data'}
    else:
        practitioner_user_profile = get_user_profile_by_user_id(practitioner)
        patient_profile = get_patient_profile_by_user_id(patient)

        existing_appointment = len(Appointment.objects.filter(patient_id=patient.id, date=booking_date, time=time).all()) != 0
        if not existing_appointment:
            if practitioner_user_profile.user_type == "doctor":
                new_appointment = Appointment.objects.create(date=booking_date,
                                                            time=time,
                                                            description=reason,
                                                            doctor_id=practitioner,
                                                            patient_id=patient_profile.id,
                                                            service_id=service_id)
            else:
                new_appointment = Appointment.objects.create(date=booking_date,
                                                            time=time,
                                                            description=reason,
                                                            nurse_id=practitioner,
                                                            patient_id=patient.id,
                                                            service_id=service_id)

            new_appointment.save()
            logger.info("New appointment created successfully for patient: " + str(patient.id) + \
                        " with practitioner: " + str(practitioner) + " on date: "  + str(booking_date) + \
                        " at time: " + str(time) + " for service: " + str(service_id) + " with reason: " + str(reason))
            data = {'success': 'true'}
        else:
            data = {'success': 'false', 'error': 'Appointment already exists'}

    return data
    

def set_invoice_status(invoice_id: int, status: bool) -> bool:
    """
    Sets the status of an invoice

    Args:
        invoice_id (int): The id of the invoice
        status (bool): The status of the invoice

    Returns:
        None
    """
    success = False
    try:
        invoice = Invoice.objects.get(invoiceID=invoice_id)
        invoice.status = status
        invoice.save()
        success = True

    except Exception as e:
        logger.info(e)
    
    return success

def get_user_type_by_id(user_id: int) -> str:
    """
    Returns the user type of a user

    Args:
        user_id (int): The id of the user

    Returns:
        str: The user type of the user
    """
    user_profile = UserProfile.objects.get(user_id=user_id)
    return user_profile.user_type