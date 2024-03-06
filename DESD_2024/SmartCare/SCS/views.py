
import json
import logging
from datetime import datetime
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from .models import DoctorProfile, NurseProfile, UserProfile, User, Timetable, Service, Appointment

from .utility import get_medical_services, check_practitioner_service , APPOINTMENT_TIMES, get_user_profile_by_user_id

logger = logging.getLogger(__name__)

def index(request):
    csrf_token = get_token(request)
    return render(request, 'index.html',{'csrf_token':csrf_token})

def Auth(request):
    return render(request, 'Auth.html')

@login_required
def Session(request):
    csrf_token = get_token(request)
    return render(request, 'CheckSession.html',{'csrf_token':csrf_token}) 



def Login(request):
    csrf_token = get_token(request)
    check = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.userprofile.user_type == user_type:
                login(request, user)
                if user_type == 'doctor':
                    return JsonResponse({'success':True,'url': 'doctor_dashboard'})
                elif user_type == 'patient':
                    return JsonResponse({'success':True,'url': 'patient_dashboard'})
                elif user_type == 'nurse':
                    return JsonResponse({'success':True,'url': 'nurse_dashboard'})
                elif user_type == 'admin':
                    return JsonResponse({'success':True,'url': 'admin_dashboard'})
            else:
                return HttpResponse("Unauthorized access", status=401)
        else:
            check = True
            messages.error(request, 'Invalid username or password')
    else:
        check = False
    return render(request, 'login.html',{'csrf_token':csrf_token,'check':check}) 



@login_required(login_url='login')
def doc(request):
    return render(request, 'doctor_dashboard.html')

@login_required(login_url='login')
def patient(request):
    
    form = AppointmentBookingForm(request.POST or None)
    services = get_medical_services()
    context = {"form": form, "services": services}
    return render(request, 'patient_dashboard.html', context)

def get_practitioners_by_day_and_service(request) -> JsonResponse:
    """
    Returns a list of practitioners available on a given day

    Args:
        request (_type_): _description_

    Returns:
        JsonResponse: A JSON response containing the list of practitioners and if the request was successful.
    """
    csrf_token = get_token(request)
    # fetch form fields

    if request.method == 'POST':
        booking_date = request.POST.get('bookingDate')
        service = request.POST.get('service')
        logger.info(f"Booking date: {booking_date}")
        logger.info(f"serviceID: {service}")

        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d")
        logger.info(f"Parsed date: {parsed_date}")

        day_of_week = parsed_date.strftime("%A").lower()
        logger.info(f"Day of week: {day_of_week}")
        

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
                logger.info(f"Doctor timetable: {doctor_timetable}")
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

        data = {'success': 'true', 'practitioners': practitioners}
    return JsonResponse(data) 


def get_time_slots_by_day_and_practitioner(request) -> JsonResponse:
    """
    Returns a list of time slots available for a given practitioner on a given day

    Args:
        request (_type_): _description_

    Returns:
        JsonResponse: A JSON response containing the list of time slots and if the request was successful.
    """
    print("Reached get_time_slots_by_day_and_practitioner")

    if request.method == 'POST':
        booking_date = request.POST.get('bookingDate')
        practitioner = request.POST.get('practitioner')

        logger.info(f"Booking date: {booking_date}")
        logger.info(f"Practitioner: {practitioner}")

        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d")
        logger.info(f"Parsed date: {parsed_date}")

        practitioner_user_profile = get_user_profile_by_user_id(practitioner)

        if practitioner_user_profile.user_type == "doctor":
            booked_appointments = Appointment.objects.filter(doctor_id=practitioner_user_profile).all()

        elif practitioner_user_profile.user_type == "nurse":
            booked_appointments = Appointment.objects.filter(nurse_id=practitioner_user_profile).all()

        time_slot_taken = False
        for appointment in booked_appointments:
            logger.info(f"Appointment dateTime: {appointment.dateTime}")
            logger.info(f"Appointment dateTime type: {type(appointment.dateTime)}")
            if appointment.dateTime == parsed_date:
                time_slot_taken = True
                break
        
        logger.info(f"Appointment dateTime: {appointment.dateTime}")
        
    return JsonResponse({'success': 'true'})

def patient_appointment_booking(request) -> JsonResponse:
    """
    View function for patient appointment booking

    Args:
        request (_type_): _description_

    Returns:
        JsonResponse: JsonResponse containing the result of the request
    """
    print("Reached patient_appointment_booking")
    csrf_token = get_token(request)
    check = False
    print(request.method)
    if request.method == 'POST':
        # fetch form fields
        booking_date = request.POST.get('bookingDate')
        logger.info(f"Booking date: {booking_date}")
        service_id = request.POST.get('service')
        logger.info(f"serviceID: {service_id}")
        practitioner = request.POST.get('practitioner')
        logger.info(f"Practitioner: {practitioner}")
        print(booking_date)

        data = {'success': 'true'}
    else:
        check = False
    return JsonResponse(data) 

@login_required(login_url='login')
def admin(request):
    return render(request, 'admin_dashboard.html')

@login_required(login_url='login')
def nurse(request):
    return render(request, 'nurse_dashboard.html')


def Logout(request):
    logout(request)
    return redirect('/login') 



def check_session(request):
    if request.user.is_authenticated:  
        return JsonResponse({'status': 'active'}, status=200)
    else:
        return JsonResponse({'status': 'expired'}, status=401)


