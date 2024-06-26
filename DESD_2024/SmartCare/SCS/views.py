import logging
import tempfile
import json
import re 
from datetime import datetime
from django.db import transaction
from django.shortcuts import render,redirect, HttpResponse, get_object_or_404, Http404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404, HttpResponseNotFound, HttpResponseNotAllowed
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.middleware.csrf import get_token
from django.utils import timezone
from django.contrib.auth.models import Group

from .models import DoctorProfile, NurseProfile, Timetable, UserProfile, Service, Appointment, Address, PatientProfile, Prescription, Invoice, PatientProfile, DoctorServiceRate, NurseServiceRate, Medication
from django.db.models import Q
from django.http import HttpResponseNotFound
from .forms import UserRegisterForm, DoctorNurseRegistrationForm, PrescriptionForm
from datetime import date


from .db_utility import get_invoices_awaiting_payment, get_invoice_information_by_user_id, \
                    get_medical_services, get_practitioners_by_day_and_service,  \
                    make_patient_appointment_booking, get_time_slots_by_day_and_practitioner, get_all_invoice_information, \
                   get_all_medications, create_invoice_for_appointment
from .utility import parse_times_for_view, get_prescriptions_for_practitioner, generate_invoice_file_content,  generate_patient_forwarding_file_content, create_report
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
                


logger = logging.getLogger(__name__)

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

@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def admin_dash(request):
    registration_form = DoctorNurseRegistrationForm()
    appointments = Appointment.objects.all()
    if request.method == 'POST':
        registration_form = DoctorNurseRegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()  # Saves the User instance

            # Determine the type of user and create corresponding profile
            user_type = registration_form.cleaned_data.get('user_type')
            if user_type == 'doctor':
                DoctorProfile.objects.create(
                    user_profile=user.profile,  # Assuming a related name or method to access UserProfile from User
                    specialization=registration_form.cleaned_data.get('specialization'),
                    isPartTime=registration_form.cleaned_data.get('isPartTime')
                )
            elif user_type == 'nurse':
                NurseProfile.objects.create(
                    user_profile=user.profile 
                )
            return redirect('dashboard')

    context = {
        'registration_form': registration_form,
        'appointments': appointments,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def register_doctor_nurse(request):
    if request.method == 'POST':
        form = DoctorNurseRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Saves the User instance
            user_type = form.cleaned_data.get('user_type')  # Fixed typo from cleaned.data to cleaned_data

            # Create UserProfile
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']

            user_profile = UserProfile(user=user, user_type = user_type, date_of_birth=date_of_birth, gender = gender)
            user_profile.save()

            number = form.cleaned_data['address_number']
            streetName = form.cleaned_data['address_street']
            city = form.cleaned_data['address_city']
            postcode = form.cleaned_data['address_postcode']
            address = Address.objects.create(number=number, streetName=streetName, city=city, postcode=postcode, user=user_profile)
            address.save()

            # Depending on the user_type, create the corresponding profile
            if user_type == 'doctor':
                doctor_profile = DoctorProfile.objects.create(
                    user_profile=user_profile,  # Refer to the just created user_profile
                    specialization=form.cleaned_data['specialization'],
                    isPartTime=form.cleaned_data['isPartTime']
                )
                doctor_profile.save()
                doctor_group = Group.objects.get(name='doctor_group')
                doctor_group.user_set.add(user)
            elif user_type == 'nurse':
                nurse_profile = NurseProfile.objects.create(
                    user_profile=user_profile  # Refer to the just created user_profile
                )
                nurse_profile.save()
                nurse_group = Group.objects.get(name='nurse_group')
                nurse_group.user_set.add(user)

            monday = True
            tuesday = True
            wednesday = True
            thursday = True
            friday = True
            saturday = False
            sunday = False
            timetable = Timetable.objects.create(practitioner = user_profile, monday = monday, tuesday = tuesday, wednesday = wednesday, thursday = thursday, friday = friday, saturday = saturday, sunday = sunday)
            timetable.save()


            return redirect('dashboard')  # Ensure 'home' is the name of your home page's URL pattern
    else:
        form = DoctorNurseRegistrationForm()

    return render(request, 'staff_register.html', {'form': form})
            
            

#fixs for the register view which takes age and first creates a user profile 
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']

            user_profile = UserProfile(user=user, user_type = 'patient', date_of_birth=date_of_birth, gender = gender)
            user_profile.save()

            allergies = form.cleaned_data['allergies']
            isPrivate = form.cleaned_data['isPrivate']

            patient_profile = PatientProfile(user_profile=user_profile, allergies = allergies, isPrivate = isPrivate)
            patient_profile.save()

            patient_group = Group.objects.get(name='patient_group')
            patient_group.user_set.add(user)

            login(request, user)

            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
                        
            number = form.cleaned_data['address_number']
            streetName = form.cleaned_data['address_street']
            city = form.cleaned_data['address_city']
            postcode = form.cleaned_data['address_postcode']
            address = Address.objects.create(number=number, streetName=streetName, city=city, postcode=postcode, user=user_profile)
            address.save()

            user_name = f"{firstname} {lastname}"
            request.session['user_name'] = user_name
            return redirect('auth')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def start_appointment(request):

    appointment_id = request.POST.get('appointmentID')

    appointment = Appointment.objects.get(appointmentID=appointment_id)
    
    service = appointment.service
    
    medications = get_all_medications()
    patient = appointment.patient
    patient_name = f"{patient.user_profile.user.first_name} {patient.user_profile.user.last_name}"

    context = {
        'appointment': appointment,
        'patient_name': patient_name,
        'patient': patient,
        'medications': medications,
        'service': service
    }
    return render(request, 'complete_appointment.html', context)

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def complete_appointment(request):
    if request.method == 'POST':

        with transaction.atomic():
            appointment_id = request.POST.get('appointmentID')
            notes = request.POST.get('notes')

            appointment = Appointment.objects.get(appointmentID=appointment_id)
            appointment.status = 'complete'
            appointment.notes = notes
            appointment.save()

            patient_id = request.POST.get('patientID')
            patient = PatientProfile.objects.get(id=patient_id)
            patient_user_profile = patient.user_profile
            
            medication = request.POST.get('medication')

           
            if medication not in [None, 'none']:
                medication = Medication.objects.get(medicationID=medication)
                dosage = request.POST.get('dosage')
                dosage = str(dosage) + "mg"

                quantity = request.POST.get('quantity')
                instructions = request.POST.get('instructions')
                repeatable = request.POST.get('repeatable')
                if repeatable:
                    repeatable = True
                else: 
                    repeatable = False

            practitioner = request.user.id

            current_date = datetime.now().date()

            if patient.isPrivate:
                create_invoice_for_appointment(appointment.appointmentID, "private")
            else:
                create_invoice_for_appointment(appointment.appointmentID, "nhs")

            practitioner_type = get_user_type(practitioner)

            if medication not in [None, 'none']:
                if practitioner_type == 'doctor':
                    doctor = DoctorProfile.objects.get(user_profile__user=request.user)
                    doctor_user_profile = doctor.user_profile
                    Prescription.objects.create(repeatable=repeatable,
                                                approved=True, 
                                                medication=medication,
                                                dosage=dosage,
                                                quantity=quantity,
                                                instructions=instructions,
                                                issueDate=current_date,
                                                appointment=appointment,
                                                patient=patient_user_profile,
                                                doctor=doctor_user_profile,
                                                nurse=None,)
                elif practitioner_type == 'nurse':
                    nurse = NurseProfile.objects.get(user_profile__user=request.user)
                    nurse_user_profile = nurse.user_profile
                    Prescription.objects.create(repeatable=repeatable,
                                                approved=True, 
                                                medication=medication,
                                                dosage=dosage,
                                                quantity=quantity,
                                                instructions=instructions,
                                                issueDate=current_date,
                                                appointment=appointment,
                                                patient=patient_user_profile,
                                                doctor=None,
                                                nurse=nurse_user_profile,
                                                )
                    
    data = {'success': 'true'}

    return JsonResponse(data) 

@login_required(login_url='login')
@custom_user_passes_test(is_patient)
def make_payment(request):
    if request.method == 'GET':
        invoice_id = request.GET.get('invoiceID')
        invoice = Invoice.objects.get(invoiceID=invoice_id)
        invoice.status = 1
        invoice.save()

    return redirect('dashboard')

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
    msg = ""
    user_type = ""
    if request.user.is_authenticated:
        user_id = request.user.id
        user_type = get_user_type(user_id)
        user_name = request.session.get('user_name')
        if user_name == "" or user_name is None:
            user = request.user
            user_name = user.get_full_name()
    else:
        user_name = ""
    
    
        
    return render(request, 'Auth.html', {'user_name':user_name, 'user_type':user_type, 'msg': msg})

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
            
            return redirect('dashboard')
            
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
    return render(request, 'doctor_dashboard.html',{'clicked':False,'clicked2':False,'user_type': user_type, 'user_name':user_name})

@login_required(login_url='login')
@custom_user_passes_test(is_patient)
def patient(request):
    invoices = get_invoice_information_by_user_id(request.user.id)
    patient_profile = PatientProfile.objects.get(user_profile__user=request.user)
    historic_appointments = Appointment.objects.filter(patient=patient_profile)
    current_date = datetime.now().date()
    services = get_medical_services()
    user_type = "patient"
    user = request.user
    user_name = user.get_full_name
    historic_prescriptions = Prescription.objects.filter(patient=patient_profile.user_profile)
    if len(historic_prescriptions) < 1:
        historic_prescriptions = None
    
    if user_name == "" or user_name is None:
        user_name = request.session.get('user_name')
        if user_name is None:
            user_name = ""
    

    context = {"services": services,
                "user_type": user_type,
                "user_name": user_name, 
                "historic_appointments": historic_appointments, 
                "historic_prescriptions": historic_prescriptions,
                "date":current_date,
                "invoices": invoices}
    
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

@login_required(login_url='login')
def retrieve_time_slots_by_day_and_practitioner(request) -> JsonResponse:
    """
    Returns a list of time slots available for a given practitioner on a given day

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: A JSON response containing the list of time slots and if the request was successful.
    """

    csrf_token = get_token(request)

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

@login_required(login_url='login')
@custom_user_passes_test(is_patient)
def patient_appointment_booking(request) -> JsonResponse:
    """
    View function for patient appointment booking

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: JsonResponse containing the result of the request
    """
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
def dashboard_resolver(request):
    """
    Function to resolve the dashboard based on the user type

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the dashboard
    """
    user_id = request.user.id
    user_type = get_user_type(user_id)
    if user_type == 'doctor':
        return doc(request)
    elif user_type == 'patient':
        return patient(request)
    elif user_type == 'nurse':
        return nurse(request)
    elif user_type == 'admin':
        return admin(request)
    else:
        return redirect('login')

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
    all_invoices = get_all_invoice_information()
    invoices_to_be_paid = get_invoices_awaiting_payment()
    doctor_service_rate = DoctorServiceRate.objects.all()
    nurse_service_rate = NurseServiceRate.objects.all()
    patient_details = PatientProfile.objects.all()
    appointments=Appointment.objects.all()
    Dates = []
    for appt in appointments:
        if appt.date and appt.date not in Dates:
            Dates.append(appt.date)
    practitioners = []
    for appt in appointments:
        if appt.doctor and appt.doctor not in practitioners:
            practitioners.append(appt.doctor)
        elif appt.nurse and appt.nurse not in practitioners:
            practitioners.append(appt.nurse)
    return render(request, 'admin_dashboard.html', {'user_type': user_type, "user_name": user_name,
                                                     "all_invoices": all_invoices, "invoices_to_be_paid": invoices_to_be_paid,
                                                     "doctor_service_rate": doctor_service_rate, "nurse_service_rate": nurse_service_rate,"practitioners": practitioners,"patients":patient_details,"appointments":appointments,"dates":Dates})

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
    return render(request, 'nurse_dashboard.html', {'user_type': user_type, "user_name": user_name,'clicked':False,'clicked2':False})

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
        user = request.user
        user_name = user.get_full_name
        user_type = 'doctor'
        return render(request, 'doctor_dashboard.html', {'appointments': appointment_details, 'patients': patient_details,'clicked':True, 'user_name':user_name, 'user_type':user_type})
    
    elif is_nurse(request.user):
        # Get the nurse's ID
        nurse_id = request.user.id
        # Retrieve the list of patients assigned to the nurse
        patients = Appointment.objects.filter(nurse_id=nurse_id).values('patient')
        patient_names = [PatientProfile.objects.get(id=patient['patient']).user_profile for patient in patients]
        
        patient_details = PatientProfile.objects.filter(user_profile__user__username__in=patient_names)
        # this query gets all the history appointments to the dashboard 
        appointment_details = Appointment.objects.all()
        user = request.user
        user_name = user.get_full_name
        user_type = 'nurse'
        
        return render(request, 'nurse_dashboard.html', {'appointments': appointment_details, 'patients': patient_details,'clicked':True, 'user_name':user_name, 'user_type':user_type})
    

    elif is_admin(request.user):
        # get all patients details and appointments regardless of the staff member allocated to them 
        patient_details = PatientProfile.objects.all()
        appointment_details = Appointment.objects.all()
        user = request.user
        user_name = user.get_full_name
        user_type = 'admin'
        return render(request,'admin_dashboard.html',{'patients':patient_details,'appointments': appointment_details, 'user_name':user_name, 'user_type':user_type})

    else:
        return HttpResponseNotFound("404 Error: Page not found")
    

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def currentAppt(request):
    if is_doctor(request.user):
        current_date = date.today()
        doctor = request.user.id 
        appointments = Appointment.objects.filter(date=current_date, doctor=doctor)
        user = request.user
        user_name = user.get_full_name
        user_type = 'doctor'
        return render(request, 'doctor_dashboard.html', {'Appointments': appointments ,'clicked2':True, 'user_name':user_name, 'user_type':user_type})
    elif is_nurse(request.user):
        current_date = date.today()
        nurse = request.user.id 
        appointments = Appointment.objects.filter(date=current_date, nurse=nurse)
        user = request.user
        user_name = user.get_full_name
        user_type = 'nurse'
        return render(request, 'nurse_dashboard.html', {'Appointments': appointments,'clicked2':True, 'user_name':user_name, 'user_type':user_type})

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def historic_appointments(request):
    if is_doctor(request.user):
        doctor = request.user.id
        historic_appointments = Appointment.objects.filter(doctor=doctor)

        return render(request, 'doctor_dashboard.html', {'historic_appointments': historic_appointments, 'clicked3':True})
    
    elif is_nurse(request.user):
        nurse = request.user.id
        historic_appointments = Appointment.objects.filter(nurse=nurse)
        return render(request, 'nurse_dashboard.html', {'historic_appointments': historic_appointments, 'clicked3':True})

@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def delete_patient(request,id):
     if request.method == 'DELETE':
        try:
            # Filter the rows per patient_id
            p_details = PatientProfile.objects.get(id=id)
          
            if (p_details):
                user_profile = p_details.user_profile
                user = user_profile.user
                p_details.delete()
                user_profile.delete()
                user.delete()
                
            else:
                return HttpResponse("Could not delete the row , please try agin", status=400)
            # Return a success response
            return HttpResponse(status=204) 
        except PatientProfile.DoesNotExist:
            # If the row doesn't exist, return a not found response
            return HttpResponse(status=404)  # 404 Not Found
     else:
       return HttpResponseNotAllowed(['DELETE'])
     
@login_required(login_url='login')
def delete_appointment(request,id):
     
     if request.method == 'DELETE':
        try:
            # Filter the rows per patient_id
            a_details = Appointment.objects.get(appointmentID=id)
          
            if (a_details):
               
                a_details.delete()
              
                
            else:
                return HttpResponse("Could not delete the row , please try agin", status=400)
            # Return a success response
            return HttpResponse(status=204) 
        except Appointment.DoesNotExist:
            # If the row doesn't exist, return a not found response
            return HttpResponse(status=404)  # 404 Not Found
     else:
       return HttpResponseNotAllowed(['DELETE'])
        
@login_required(login_url='login')
def update_patient(request):
    if request.method == 'POST':
        # Get the rowId from the POST data
        id = request.POST.get('id')
        name = request.POST.get('Name')
        allergies = request.POST.get('Allergies')
        isPrivate = request.POST.get('Status')


        if not re.match(r"^[A-Za-z.]+$", name) :
            return JsonResponse({'success': False, 'message': 'Invalid name format'})


        # Allergies validation 
        elif not re.match(r"^[A-Za-z.]+$", allergies) :
            return JsonResponse({'success': False, 'message': 'Invalid format for the allergie field'})

        try:
            
            model_instance = PatientProfile.objects.get(id=id)
          
            user_instance = UserProfile.objects.get(user__username=model_instance.user_profile.user.username)
          
            user_instance.user.username = name 
            user_instance.user.save()
          
            model_instance.user_profile = user_instance

            model_instance.allergies = allergies
            model_instance.isPrivate = isPrivate
        
            
            # Save the changes to the model instance
            model_instance.save()
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True ,'data':{
                'name': model_instance.user_profile.user.username,
                 'allergies': model_instance.allergies,
                 'status': model_instance.isPrivate }
                 }
            )
        
        except PatientProfile.DoesNotExist:
            # Return a JSON response indicating failure if the model instance does not exist
            return JsonResponse({'success': False, 'message': 'Model instance does not exist'})
        except UserProfile.DoesNotExist:
            # Return a JSON response indicating failure if the model instance does not exist
            return JsonResponse({'success': False, 'message': 'Model instance does not exist'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def prescription_approval(request):
    if is_doctor(request.user):
        doctor = request.user.id
        pending_prescriptions = Prescription.objects.filter(approved=False)
        return render(request, 'doctor_dashboard.html', {'pending_prescriptions': pending_prescriptions, 'clicked4':True})
    
    elif is_nurse(request.user):
        nurse = request.user.id
        pending_prescriptions = Prescription.objects.filter(approved=False)
        return render(request, 'nurse_dashboard.html', {'pending_prescriptions': pending_prescriptions, 'clicked4':True})


@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def historic_prescriptions(request):
    if is_doctor(request.user):
        doctor = request.user.id
        historic_prescriptions = Prescription.objects.all()

        return render(request, 'doctor_dashboard.html', {'historic_prescriptions': historic_prescriptions, 'clicked5':True})
    
    elif is_nurse(request.user):
        nurse = request.user.id
        historic_prescriptions = Prescription.objects.all()

        return render(request, 'nurse_dashboard.html', {'historic_prescriptions': historic_prescriptions, 'clicked5':True})

@login_required(login_url='login')
@custom_user_passes_test(is_doctor_or_nurse)
def approve_prescription(request):
    if is_doctor(request.user):
        if request.method == 'POST':
            prescription_id = request.POST.get('prescriptionID')
            prescription = Prescription.objects.get(prescriptionID=prescription_id)
            prescription.approved = True
            prescription.issueDate = timezone.now().date()
            prescription.reissueDate = timezone.now().date() + timezone.timedelta(days=30)
            prescription.save()
            return render(request, 'doctor_dashboard.html')
    elif is_nurse(request.user):
        if request.method == 'POST':
            prescription_id = request.POST.get('prescriptionID')
            prescription = Prescription.objects.get(prescriptionID=prescription_id)
            prescription.approved = True
            prescription.issueDate = timezone.now().date()
            prescription.reissueDate = timezone.now().date() + timezone.timedelta(days=30)
            prescription.save()
            return render(request, 'nurse_dashboard.html')
    else:
        return JsonResponse({'success': 'false', 'error': 'Invalid request method'})

@login_required(login_url='login')
def filter_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        isPrivate = data.get('Bill')
        logger.info(isPrivate)
        print(isPrivate)

        if isPrivate == False:
            patients = PatientProfile.objects.filter(isPrivate=False)
        elif isPrivate == True:
            patients = PatientProfile.objects.filter(isPrivate=True)
        else:
            patients = PatientProfile.objects.all()

        patient_data = [{'name': patient.user_profile.user.username, 'allergies': patient.allergies, 'isPrivate': patient.isPrivate } for patient in patients]
        return JsonResponse({'success':True,'data': patient_data})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
   
@login_required(login_url='login')
def filter_appointments(request):
    if request.method =='POST':
        data = json.loads(request.body)
        selectedDate = data['date']
        selectedEmployee = data['employee']  
        selectedDate = datetime.strptime(selectedDate, '%B %d, %Y').strftime('%Y-%m-%d')  
        try:
            
            user = User.objects.get(username=selectedEmployee)
            user_profile = UserProfile.objects.get(user=user)
            

            filtered_appointments = Appointment.objects.filter(Q(date=selectedDate) & (Q(nurse=user_profile) | Q(doctor=user_profile)))
            filt_app = [{'ID': appt.appointmentID, 'date': appt.date, 'time': appt.time,'service':appt.service.service,'practitioner':selectedEmployee } for appt in filtered_appointments]
            return JsonResponse({'success':True,'data': filt_app})    
        except ObjectDoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def generate_invoice(request):
    """
    Function to generate an invoice

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the invoice
    """
    csrf_token = get_token(request)
    if request.method == 'GET':
        user_id = request.user.id
        patient = PatientProfile.objects.filter(user_profile_id=user_id).first()
        invoice_id = request.GET.get('invoiceID')

        # Check if the invoice belongs to the user
        invoice = Invoice.objects.filter(invoiceID=invoice_id).first()

        if invoice is None:
            raise Http404("Resource not found")
        if is_admin(request.user):
            pass
        else:
            if invoice.patient_id != patient.id:
                raise Http404("Resource not found")
        
        # generate invoice file content and name
        file_content, file_name = generate_invoice_file_content(invoice_id)
        bytes_data = bytes(file_content, 'utf-8')

        # creating temp file to serve
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(bytes_data)
            temp_file.flush()

            # Get the file path
            file_path = temp_file.name

            # Serve the temporary file
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response

#? More protection?
@login_required(login_url='login')
def generate_patient_forwarding_file(request):
    """
    Function to generate a forwarding file for a patient

    Args:
        request (HttpRequest): Django view request object

    Returns:
        HttpResponse: Page response containing the invoice
    """
    csrf_token = get_token(request)
    if request.method == 'GET':
        user_profile_id = request.GET.get('userProfileID')
        patient = PatientProfile.objects.filter(user_profile_id=user_profile_id).first()
        
        # generate invoice file content and name
        file_content, file_name = generate_patient_forwarding_file_content(patient)
        bytes_data = bytes(file_content, 'utf-8')

        # creating temp file to serve
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(bytes_data)
            temp_file.flush()

            # Get the file path
            file_path = temp_file.name

            # Serve the temporary file
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response


@login_required(login_url='login')
def prescription_pending_approval(request):
    """
    Function to handle prescription pending approval
    
    Args:
        request (HttpRequest): Django view request object
        
    Returns:
        JsonResponse: JSON response containing the prescription pending approval
    """
    
    user = request.user
    prescriptions = get_prescriptions_for_practitioner(user)
    if prescriptions is not None:
        pending_prescriptions = [prescription for prescription in prescriptions if prescription.approved == False and prescription.repeatable == True]
        prescriptions_data = [
            {
                'prescriptionID': prescription.prescriptionID,
                'repeatable': prescription.repeatable,
                'medication': prescription.medication.name,
                'dosage': prescription.dosage,
                'quantity': prescription.quantity,
                'instructions': prescription.instructions,
                'issueDate': prescription.issueDate.strftime('%Y-%m-%d %H:%M:%S'),
                'reissueDate': prescription.reissueDate.strftime('%Y-%m-%d %H:%M:%S'),
                'appointment': prescription.appointment.id,
                'patient': prescription.patient.user.username,
                'doctor': prescription.doctor.user.username if prescription.doctor else None,
                'nurse': prescription.nurse.user.username if prescription.nurse else None
            }
        for prescription in pending_prescriptions
        ]
        data = {'success': 'true', 'prescriptions': prescriptions_data}
    else:
        data = {'success': 'false', 'error': 'User is not a doctor or Nurse'}
    return JsonResponse(data)

@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def mark_invoice_as_paid(request):
    """
    Function to mark an invoice as paid

    Args:
        request (HttpRequest): Django view request object

    Returns:
        JsonResponse: JSON response containing the result of the request
    """

    csrf_token = get_token(request)
    if request.method == 'POST':
        admin_user = request.user

        if is_admin(admin_user):
           
            invoice_id = request.POST.get('invoice_id')
            invoice = Invoice.objects.get(invoiceID=invoice_id)
           
            invoice.status = 1
            invoice.approved = 1
          
            invoice.save()

            data = {'success': 'true'}
        # redirect to 404 if the user is not an admin
        else:
            return redirect(Http404)
    else:
        data = {'success': 'false'}
    return redirect('dashboard')



@login_required(login_url='login')
@custom_user_passes_test(is_patient)
def request_repeat_prescription(request):
    if request.method == 'POST':
        prescription_id = request.POST.get('prescription_id')
        existing_prescription = get_object_or_404(Prescription, prescriptionID=prescription_id)
        new_prescription_data = {
            'repeatable': existing_prescription.repeatable,
            'medication': existing_prescription.medication,
            'dosage': existing_prescription.dosage,
            'quantity': existing_prescription.quantity,
            'instructions': existing_prescription.instructions,
            'patient': existing_prescription.patient,
            'doctor': existing_prescription.doctor,
            'nurse': existing_prescription.nurse,
            'approved': False,
            'issueDate': date.today(),
            'reissueDate': None,
            'appointment': existing_prescription.appointment,
        }

        form = PrescriptionForm(new_prescription_data)
        if form.is_valid():
            existing_prescription.repeatable = False
            existing_prescription.save()

            prescription = form.save()


            return redirect('dashboard')  # Redirect to another page after object creation
        else:
            # Return a JsonResponse with the form errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # Handle GET request if needed
        pass

@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def update_doctor_service_rate(request):
    if request.method == 'POST':
        doctorServiceRateID = request.POST.get('doctorServiceRateID')
        new_rate = request.POST.get('rate')

        doctor_service_rate = get_object_or_404(DoctorServiceRate, doctorServiceRateID=doctorServiceRateID)
        doctor_service_rate.rate = new_rate
        doctor_service_rate.save()
        return redirect('dashboard')
    else:
        pass

@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def update_nurse_service_rate(request):
    if request.method == 'POST':
        nurseServiceRateID = request.POST.get('nurseServiceRateID')
        new_rate = request.POST.get('rate')

        nurse_service_rate = get_object_or_404(NurseServiceRate, nurseServiceRateID=nurseServiceRateID)
        nurse_service_rate.rate = new_rate
        nurse_service_rate.save()
        return redirect('dashboard')
    else:
        pass


@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def ADM_delete_appointment(request,id):
     
     if request.method == 'DELETE':
        try:
            
            a_details = Appointment.objects.get(appointmentID=id)
          
            if (a_details):
               
                a_details.delete()
              
                
            else:
                return HttpResponse("Could not delete the row , please try agin", status=400)
            # Return a success response
            return HttpResponse(status=204) 
        except Appointment.DoesNotExist:
            # If the row doesn't exist, return a not found response
            return HttpResponse(status=404)  # 404 Not Found
     else:
       return HttpResponseNotAllowed(['DELETE'])
     
@login_required(login_url='login')
@custom_user_passes_test(is_admin)
def generate_report(request):
    file_name = None
    if request.method == 'POST':
        start_date_input = request.POST.get('start_date')
        end_date_input = request.POST.get('end_date')

        start_date = datetime.strptime(start_date_input, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_input, '%Y-%m-%d').date()

        file_name = create_report(start_date, end_date)

        file_path = f"/code/SmartCare/Reports/{file_name}"
        return FileResponse(open(file_path, 'rb'))
    else:
        pass
