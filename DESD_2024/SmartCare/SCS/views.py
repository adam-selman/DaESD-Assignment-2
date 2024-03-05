
import json
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .forms import AppointmentBookingForm
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token
from .models import DoctorProfile, NurseProfile, UserProfile, User


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
    booking_date = request.POST.get('bookingDate')

    all_doctors = DoctorProfile.objects.all()
    all_nurses = NurseProfile.objects.all()
    doctors = []
    nurses = []

    for doctor in all_doctors:
        doctor_user_profile = UserProfile.objects.filter(id=doctor.user_profile_id).first()
        doctor_user_info = User.objects.filter(id=doctor_user_profile.user_id).first()
        doctors.append((doctor_user_info.first_name + " " + doctor_user_info.last_name, doctor_user_info.id))
   
    for nurse in all_nurses:
            nurse_user_profile = UserProfile.objects.filter(id=nurse.user_profile_id).first()
            nurse_user_info = User.objects.filter(id=nurse_user_profile.user_id).first()
            nurses.append((nurse_user_info.first_name + " " + nurse_user_info.last_name, nurse_user_info.id))

    practitioners = {"doctors": doctors,
                    "nurses": nurses}

    data = {'success': 'true', 'practitioners': practitioners}
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

