from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
#from .forms import LoginForm
from django.contrib.auth import authenticate, login , logout
from django.middleware.csrf import get_token, rotate_token
from django.middleware import csrf
from .models import UserProfile
from django.contrib.auth.decorators import user_passes_test


def is_doctor(user):
    return user.groups.filter(name='doctor_group').exists()

def is_nurse(user):
    return user.groups.filter(name='nurse_group').exists()

def is_patient(user):
    return user.groups.filter(name='patient_group').exists()

def is_admin(user):
    return user.groups.filter(name='admin_group').exists()

def index(request):
    csrf_token = get_token(request)
    return render(request, 'index.html',{'csrf_token':csrf_token})

def Auth(request):
    return render(request, 'Auth.html')

def Session(request):
    csrf_token = get_token(request)
    return render(request, 'CheckSession.html',{'csrf_token':csrf_token}) 



def Login(request):
    csrf_token = csrf.get_token(request)
    check = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        

        user = authenticate(username=username, password=password)
        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            user_type = user_profile.user_type
            
            login(request, user)
            #####rotate_token(request)
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
    return render(request, 'doctor_dashboard.html')

@login_required(login_url='login')
@user_passes_test(is_patient, login_url='login')
def patient(request):
    return render(request, 'patient_dashboard.html')

@login_required(login_url='login')
@user_passes_test(is_admin, login_url='login')
def admin(request):
    return render(request, 'admin_dashboard.html')

@login_required(login_url='login')
@user_passes_test(is_nurse, login_url='login')
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


