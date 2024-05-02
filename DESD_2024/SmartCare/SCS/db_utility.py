from enum import Enum
from datetime import datetime
import logging 
import copy 

from .models import Service, Invoice, DoctorServiceRate, Timetable, NurseServiceRate, User, DoctorProfile, NurseProfile, UserProfile, Appointment, PatientProfile, Medication


logger = logging.getLogger(__name__)


class BILLABLE_PARTIES(Enum):
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
    else:
        raise ValueError("Appointment must have a doctor or a nurse")
    if doctor:
        doctor_service_rate_object = DoctorServiceRate.objects.get(service_id=service_id) 
        service_rate = doctor_service_rate_object.rate
    else:
        nurse_service_rate_object = NurseServiceRate.objects.get(service_id=service_id)
        service_rate = nurse_service_rate_object.rate
        
    return service_rate


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

    if billing_party not in ["NHS", "Private", "nhs", "private"]:
        raise ValueError("Billing party must be NHS, Insurance or Private.")

    amount = calculate_appointment_cost(appointment_id)
    appointment = Appointment.objects.get(appointmentID=appointment_id)

    previous_invoice = Invoice.objects.filter(appointment_id=appointment_id).first()

    # check if invoice exists for given appointment
    if previous_invoice is not None:
        
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
    
    patient_profile = get_patient_profile_by_user_id(user_id)
    invoices = Invoice.objects.filter(patient_id=patient_profile.id).all()
    invoice_info = []
    for invoice in invoices:
        service = get_service_by_appointment_id(invoice.appointment_id)
        service_name = service.service.title()
        amount = invoice.amount
        issue_date = invoice.dateIssued.strftime("%d-%m-%Y")
        invoice_info.append([service_name, amount, issue_date, invoice.invoiceID, invoice.status, invoice.approved])
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
        invoice_info.append([service_name, amount, issue_date, invoice.invoiceID, invoice.status, invoice.approved])
    return invoice_info

def get_invoices_awaiting_payment() -> list:
    """
    Returns a list of invoices awaiting payment

    Returns:
        list: A list of invoices awaiting payment
    """
    invoices = Invoice.objects.filter(approved=False).all()
    invoice_info = []
    for invoice in invoices:
        service = get_service_by_appointment_id(invoice.appointment_id)
        service_name = service.service.title()
        amount = invoice.amount
        issue_date = invoice.dateIssued.strftime("%d-%m-%Y")
        if invoice.approved == 0:
            invoice_info.append([service_name, amount, issue_date, invoice.invoiceID, invoice.status, invoice.approved])
    
    
    return invoice_info

def get_patient_profile_by_user_profile(user_profile: int) -> PatientProfile:
    """
    Returns the patient profile

    Args:
        user_profile_id (int): The user profile id

    Returns:
        PatientProfile: The patient profile of the user
    """
    patient_profile = PatientProfile.objects.get(user_profile_id=user_profile.id)
    return patient_profile

def get_all_appointments_by_patient_profile(patient_profile) -> list:
    """
    Returns all appointments for a patient

    Returns:
        list: The appointments for the patient
    """
    appointments = Appointment.objects.filter(patient_id=patient_profile.id).all()
    return appointments

def get_doctor_profile_by_user_profile_id(user_profile_id: int) -> DoctorProfile:
    """
    Returns the doctor profile

    Args:
        user_profile_id (int): The user profile id

    Returns:
        DoctorProfile: The doctor profile of the user
    """
    doctor_profile = DoctorProfile.objects.get(user_profile_id=user_profile_id)
    return doctor_profile

def get_nurse_profile_by_user_profile_id(user_profile_id: int) -> NurseProfile:
    """
    Returns the nurse profile

    Args:
        user_profile_id (int): The user profile id

    Returns:
        NurseProfile: The nurse profile of the user
    """
    nurse_profile = NurseProfile.objects.get(user_profile_id=user_profile_id)
    return nurse_profile

def get_all_medications() -> list:
    """
    Returns all medication

    Returns:
        list: A list of all medication
    """
    medication = Medication.objects.all()
    return medication

def get_user_by_user_profile(user_profile: int) -> User:
    """
    Returns the user

    Args:
        user_profile_id (int): The user profile id

    Returns:
        User: The user of the user profile
    """
    user = User.objects.get(id=user_profile.user_id)
    return user

def get_practitioner_name_by_user_profile_id(user_profile_id: int) -> str:
    """
    Returns the name of a practitioner

    Args:
        user_profile_id (int): The user profile id

    Returns:
        str: The name of the practitioner
    """
    user_profile = UserProfile.objects.get(id=user_profile_id)
    user = User.objects.get(id=user_profile.user_id)
    user_type = get_user_type_by_id(user.id)

    if user_type == "doctor":
        name = "Dr. " + user.first_name + " " + user.last_name
    elif user_type == "nurse":
        name = "Nurse " + user.first_name + " " + user.last_name
    return name

def get_patient_appointments_by_user_id(user_id: int, future=False, past=False) -> list:
    """
    Returns the appointments for a patient

    Args:
        user_id (int): The user id

    Returns:
        list: The appointments for the patient
    """
    
    user_profile = get_user_profile_by_user_id(user_id)
    
    patient_profile = get_patient_profile_by_user_profile(user_profile)
    appointments = get_all_appointments_by_patient_profile(patient_profile)
    appointment_info = []
    for appointment in appointments:
        service = get_service_by_appointment_id(appointment.appointmentID)
        service_name = service.service.title()

        practitioner_name = get_practitioner_name_by_user_profile_id(appointment.doctor_id)

        if future:
            if appointment.date >= datetime.now().date():
                appointment_info.append([service_name, appointment.date, appointment.time, appointment.appointmentID, practitioner_name])
        if past:
            if appointment.date < datetime.now().date():
                appointment_info.append([service_name, appointment.date, appointment.time, appointment.appointmentID, practitioner_name])
        else:
            appointment_info.append([service_name, appointment.date, appointment.time, appointment.appointmentID, practitioner_name])
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
                                                            patient_id=patient_profile.id,
                                                            service_id=service_id)

            new_appointment.save()
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