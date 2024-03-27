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
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from .models import DoctorProfile, NurseProfile, UserProfile, User, Timetable, Service, Appointment, PatientProfile
from .forms import UserRegisterForm, DoctorNurseRegistrationForm
from datetime import date

from .models import DoctorProfile, NurseProfile, UserProfile, User, Timetable, Service, Appointment

from .utility import get_medical_services, check_practitioner_service , APPOINTMENT_TIMES, get_user_profile_by_user_id, parse_times_for_view

logger = logging.getLogger(__name__)
def register_doctor_nurse(request):
    if request.method == 'POST':
        form = DoctorNurseRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned.data.get('user_type')
            UserProfile.objects.create(user=user, user_type=user_type)
            if user_type == 'doctor':
                DoctorProfile.objects.create(
                    user_profile=user.userprofile,
                    specialization=form.cleaned_data['specialization'],
                    isPartTime=form.cleaned_data['isPartTime']
                )
            elif user_type == 'nurse':
                NurseProfile.objects.create(user_profile=user.userprofile)
            return redirect('home')
        else:
            form = DoctorNurseRegistrationForm()
        return render(request, 'staff_register.html', {'form': form})
            

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile for the new user
            profile = UserProfile(user=user, user_type='patient')
            profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def is_doctor(user):
    return user.groups.filter(name='doctor_group').exists()

def is_nurse(user):
    return user.groups.filter(name='nurse_group').exists()

def is_patient(user):
    return user.groups.filter(name='patient_group').exists()

def is_admin(user):
    return user.groups.filter(name='admin_group').exists()

def is_doctor_or_nurse_or_admin(user):
    return user.groups.filter(name__in=['doctor_group', 'nurse_group','admin_group']).exists()

def is_doctor_or_nurse(user):
    return user.groups.filter(name__in=['doctor_group', 'nurse_group']).exists()

def custom_user_passes_test(test_func):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseNotFound("404 Error: Page does not exist")
        return wrapper
    return decorator

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

def get_user_type(user_id):
    try:
        # Retrieve the user profile associated with the user_id
        user_profile = UserProfile.objects.get(user_id=user_id)
        
        # Access the user type from the user profile
        user_type = user_profile.user_type
        
        return user_type
    except UserProfile.DoesNotExist:
        return None  # Handle case where user profile does not exist for the given user ID

def Auth(request):
    """
    View function for the authentication page

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the authentication page
    """
    user_type = ""
    if request.user.is_authenticated:
        user = request.user
        user_id = request.user.id
        user_name = user.get_full_name()
        user_type = get_user_type(user_id)
        if user_type is None:
            user_type = ""
    else:
        user_name = ""
    
    
        
    return render(request, 'Auth.html', {'user_name':user_name, 'user_type':user_type})

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
@custom_user_passes_test(is_doctor)
def doc(request):
    """
    View function for the doctor dashboard

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the doctor dashboard
    """
    user_type = "doctor"
    user = request.user
    user_name = user.get_full_name
    return render(request, 'doctor_dashboard.html',{'clicked':False,'clicked2':False}, {'user_type': user_type, 'user_name':user_name})

@login_required(login_url='login')
@custom_user_passes_test(is_patient)
def patient(request):
    services = get_medical_services()
    user_type = "patient"
    user = request.user
    user_name = user.get_full_name
    context = {"services": services, "user_type": user_type, "user_name": user_name}
    return render(request, 'patient_dashboard.html', context)

@login_required(login_url='login')
def get_practitioners_by_day_and_service(request) -> JsonResponse:
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

        data = {'success': 'true', 'practitioners': practitioners}
    return JsonResponse(data) 


def get_time_slots_by_day_and_practitioner(request) -> JsonResponse:
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

        practitioner_user_profile = get_user_profile_by_user_id(practitioner)

        # Get the appointments for the practitioner on the given day
        if practitioner_user_profile.user_type == "doctor":
            booked_appointments = Appointment.objects.filter(doctor_id=practitioner_user_profile, date=parsed_date).all()

        elif practitioner_user_profile.user_type == "nurse":
            booked_appointments = Appointment.objects.filter(nurse_id=practitioner_user_profile, date=parsed_date).all()

        booked_times = []
        # Get the booked times
        for appointment in booked_appointments:
            booked_times.append([appointment.time, appointment.duration_id])
        
        
        available_times = copy.deepcopy(APPOINTMENT_TIMES)

        # Remove booked times from available times
        for time, duration in booked_times:
            if time in available_times:
                # Remove the time and the following n times based on the duration
                index = available_times.index(time)
                for i in range(duration):
                    available_times.pop(index + i)
        if booking_date == current_date:
            # removing invalid times
            times_to_remove = []
            for time in available_times:
                # removing times before now
                if time < current_time:
                    times_to_remove.append(time)

            for time in times_to_remove:
                available_times.remove(time)

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

        if booking_date is None or service_id is None or practitioner is None or time is None or reason is None:
            data = {'success': 'false', 'error': 'Invalid form data'}
        else:
            practitioner_user_profile = get_user_profile_by_user_id(practitioner)

            existing_appointment = len(Appointment.objects.filter(patient_id=patient.id, date=booking_date, time=time).all()) != 0
            if not existing_appointment:
                if practitioner_user_profile.user_type == "doctor":
                    new_appointment = Appointment.objects.create(date=booking_date,
                                                                time=time,
                                                                description=reason,
                                                                doctor_id=practitioner,
                                                                patient_id=patient.id,
                                                                service_id=service_id,
                                                                duration_id=service_id)
                else:
                    new_appointment = Appointment.objects.create(date=booking_date,
                                                                time=time,
                                                                description=reason,
                                                                doctor_id=practitioner,
                                                                patient_id=patient.id,
                                                                service_id=service_id,
                                                                duration=service_id)

                new_appointment.save()
                logger.info("New appointment created successfully for patient: " + str(patient.id) + \
                            " with doctor: " + str(practitioner) + " on date: "  + str(booking_date) + \
                            " at time: " + str(time) + " for service: " + str(service_id) + " with reason: " + str(reason))
                data = {'success': 'true'}
            else:
                data = {'success': 'false', 'error': 'Appointment already exists'}
    else:
        check = False
    return JsonResponse(data) 

@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def admin(request):
    """
    View function for the admin dashboard

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the admin dashboard
    """
    user_type = "admin"
    user = request.user
    user_name = user.get_full_name
    return render(request, 'admin_dashboard.html', {'user_type': user_type, "user_name": user_name})

@login_required(login_url='login')
@custom_user_passes_test(is_nurse)
def nurse(request):
    """
    View function for the nurse dashboard

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the nurse dashboard
    """
    user_type = "nurse"
    user = request.user
    user_name = user.get_full_name
    return render(request, 'nurse_dashboard.html', {'user_type': user_type, "user_name": user_name},{'clicked':False,'clicked2':False})

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse_or_admin)
def display_patients(request):
    if is_doctor(request.user):
        # Get the doctor's ID
        doctor_id = request.user.id
        # Retrieve the list of patients assigned to the doctor
        patients = Appointment.objects.filter(doctor_id=doctor_id).values('patient')
        # Retrieve the patient details
        patient_names = [PatientProfile.objects.get(id=patient['patient']).user_profile for patient in patients]
        
        patient_details = PatientProfile.objects.filter(user_profile__user__username__in=patient_names)
       # this query gets all the history appointments to the dashboard 
        appointment_details = Appointment.objects.all()
        # Render the doctor dashboard template
        return render(request, 'doctor_dashboard.html', {'appointments': appointment_details, 'patients': patient_details,'clicked':True})
    
    elif is_nurse(request.user):
        # Get the nurse's ID
        nurse_id = request.user.id
        # Retrieve the list of patients assigned to the nurse
        patients = Appointment.objects.filter(nurse_id=nurse_id).values('patient')
        patient_names = [PatientProfile.objects.get(id=patient['patient']).user_profile for patient in patients]
        
        patient_details = PatientProfile.objects.filter(user_profile__user__username__in=patient_names)
        # this query gets all the history appointments to the dashboard 
        appointment_details = Appointment.objects.all()

        
        return render(request, 'nurse_dashboard.html', {'appointments': appointment_details, 'patients': patient_details,'clicked':True})
    

    elif is_admin(request.user):
        # get all patients details and appointments rregardless of the staff memeber allocated to them 
        patient_details = PatientProfile.objects.all()
        appointment_details = Appointment.objects.all()
        return render(request,'admin_dashboard.html',{'patients':patient_details,'appointments': appointment_details})

    else:
        return HttpResponseNotFound("404 Error: Page not found")
    

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def currentAppt(request):
    if is_doctor(request.user):
        current_date = date.today()
        doctor = request.user.id 
        appointments = Appointment.objects.filter(date=current_date, doctor=doctor)

        return render(request, 'doctor_dashboard.html', {'Appointments': appointments ,'clicked2':True})
    elif is_nurse(request.user):
        current_date = date.today()
        nurse = request.user.id 
        appointments = Appointment.objects.filter(date=current_date, nurse=nurse)

        return render(request, 'nurse_dashboard.html', {'Appointments': appointments,'clicked2':True})








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


