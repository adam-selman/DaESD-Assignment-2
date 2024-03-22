import copy
import json
import logging
from datetime import datetime
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.middleware.csrf import get_token

from django.contrib.auth.decorators import user_passes_test

from .models import DoctorProfile, NurseProfile, UserProfile, User, Timetable, Service, Appointment, Invoice


from .db_utility import get_service_by_appointment_id, check_practitioner_service, get_invoice_information_by_user_id, \
                    get_medical_services, get_user_profile_by_user_id, get_practitioners_by_day_and_service,  \
                         make_patient_appointment_booking, get_time_slots_by_day_and_practitioner
from .utility import APPOINTMENT_TIMES, parse_times_for_view, calculate_appointment_cost

logger = logging.getLogger(__name__)

def is_doctor(user):
    return user.groups.filter(name='doctor_group').exists()

def is_nurse(user):
    return user.groups.filter(name='nurse_group').exists()

def is_patient(user):
    return user.groups.filter(name='patient_group').exists()

def is_admin(user):
    return user.groups.filter(name='admin_group').exists()

def index(request):
    """
    View function for the index page

    Args:
        request (HttpRequest): Django view request object 

    Returns:
        HttpResponse: Page response containing the index page
    """
    csrf_token = get_token(request)
    return render(request, 'index.html',{'csrf_token':csrf_token})

def Auth(request):
    """
    View function for the authentication page

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the authentication page
    """
    return render(request, 'Auth.html')

@login_required
def Session(request):
    """
    Function to check the session status

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the session status
    """
    csrf_token = get_token(request)
    return render(request, 'CheckSession.html',{'csrf_token':csrf_token}) 

def Login(request):

    """
    Function to handle user login

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the login page
    """
    csrf_token = get_token(request)
    check = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = authenticate(username=username, password=password)
        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            user_type = user_profile.user_type
            
            login(request, user)
        
            if user_type == 'doctor':
                return redirect('docDash')
            elif user_type == 'patient':
                return redirect('patDash')
            elif user_type == 'nurse':
                return redirect('nursDash')
            elif user_type == 'admin':
                return redirect('admDash')
            
            
        else:
            check = True
            messages.error(request, 'Invalid username or password')
            
    else:
        check = False
    return render(request, 'login.html',{'csrf_token':csrf_token,'check':check}) 

@login_required(login_url='login')
@user_passes_test(is_doctor, login_url='login')
def doc(request):
    """
    View function for the doctor dashboard

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the doctor dashboard
    """
    return render(request, 'doctor_dashboard.html')

@login_required(login_url='login')
@user_passes_test(is_patient, login_url='login')
def patient(request):
    invoices = get_invoice_information_by_user_id(request.user.id)
    logger.info(f"Invoices: {invoices}")
    services = get_medical_services()
    context = {"services": services, "invoices": invoices}
    return render(request, 'patient_dashboard.html', context)

@login_required(login_url='login')
def retrieve_practitioners_by_day_and_service(request) -> JsonResponse:
    """
    Returns a list of practitioners available on a given day

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: A JSON response containing the list of practitioners and if the request was successful.
    """
    csrf_token = get_token(request)
    # fetch form fields

    if request.method == 'POST':
        booking_date = request.POST.get('bookingDate')
        service = request.POST.get('service')
        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d")

        day_of_week = parsed_date.strftime("%A").lower()

        practitioners = get_practitioners_by_day_and_service(service, day_of_week)

        data = {'success': 'true', 'practitioners': practitioners}
    return JsonResponse(data) 


def retrieve_time_slots_by_day_and_practitioner(request) -> JsonResponse:
    """
    Returns a list of time slots available for a given practitioner on a given day

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: A JSON response containing the list of time slots and if the request was successful.
    """

    if request.method == 'POST':
        booking_date = request.POST.get('bookingDate')
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().time()
        if booking_date < current_date:
            return JsonResponse({'success': 'false', 'error': 'Invalid date'})

        practitioner = request.POST.get('practitioner')

        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d")

        available_times = get_time_slots_by_day_and_practitioner(practitioner, parsed_date)
        available_times = parse_times_for_view(available_times)

    return JsonResponse({'success': 'true', 'timeSlots': available_times})

def patient_appointment_booking(request) -> JsonResponse:
    """
    View function for patient appointment booking

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: JsonResponse containing the result of the request
    """
    print("Reached patient_appointment_booking")
    csrf_token = get_token(request)
    check = False
    print(request.method)
    if request.method == 'POST':
        # fetch form fields
        patient = request.user
        booking_date = request.POST.get('bookingDate')
        service_id = request.POST.get('service')
        service = Service.objects.filter(pk=service_id).first()
        practitioner = request.POST.get('practitioner')
        time = request.POST.get('timeSlot')
        reason = request.POST.get('reason')

        data = make_patient_appointment_booking(patient, booking_date, service_id, practitioner, time, reason)
    else:
        check = False
    return JsonResponse(data) 

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin(request):
    """
    View function for the admin dashboard

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the admin dashboard
    """
    return render(request, 'admin_dashboard.html')

@login_required(login_url='login')
@user_passes_test(is_nurse, login_url='login')
def nurse(request):
    """
    View function for the nurse dashboard

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the nurse dashboard
    """
    return render(request, 'nurse_dashboard.html')


def Logout(request):
    """
    Function to handle user logout

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the login page
    """
    logout(request)
    return redirect('/login') 



def check_session(request):
    """
    Function to check the session status

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: JSON response containing the session status
    """
    if request.user.is_authenticated:  
        return JsonResponse({'status': 'active'}, status=200)
    else:
        return JsonResponse({'status': 'expired'}, status=401)


