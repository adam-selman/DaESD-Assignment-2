
import json
import logging
from datetime import datetime
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .forms import AppointmentBookingForm
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from .models import DoctorProfile, NurseProfile, UserProfile, User, Timetable

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def Auth(request):
    return render(request, 'Auth.html')

 


@login_required
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

def patient(request):
    
    form = AppointmentBookingForm(request.POST or None)
    context = {"form": form}
    return render(request, 'patient_dashboard.html', context)

def get_practitioners(request) -> JsonResponse:

    print("Reached patient_appointment_booking")
    csrf_token = get_token(request)
    # fetch form fields

    if request.method == 'POST':
        booking_date = request.POST.get('bookingDate')
        logger.info(f"Booking date: {booking_date}")

        parsed_date = datetime.strptime(booking_date, "%Y-%m-%d")
        logger.info(f"Parsed date: {parsed_date}")

        day_of_week = parsed_date.strftime("%A").lower()
        logger.info(f"Day of week: {day_of_week}")
        

        all_doctors = DoctorProfile.objects.all()
        all_nurses = NurseProfile.objects.all()
        doctors = []
        nurses = []

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
    
        for nurse in all_nurses:
            nurse_user_profile = UserProfile.objects.filter(id=nurse.user_profile_id).first()
            nurse_user_info = User.objects.filter(id=nurse_user_profile.user_id).first()
            nurse_timetable = Timetable.objects.filter(practitioner_id=nurse.user_profile_id).first()
            logger.info(f"nurse timetable: {nurse_timetable}")
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

        data = {'success': 'true', 'practitioners': practitioners, "day_of_week": day_of_week}
    return JsonResponse(data) 


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
        print(booking_date)

        data = {'success': 'false', 'bookingDate': booking_date}
    else:
        check = False
    return JsonResponse(data) 

@login_required
def admin(request):
    return render(request, 'admin_dashboard.html')

@login_required
def nurse(request):
    return render(request, 'nurse_dashboard.html')

