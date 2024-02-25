from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
#from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.middleware.csrf import get_token


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

@login_required
def patient(request):
    return render(request, 'patient_dashboard.html')

@login_required
def admin(request):
    return render(request, 'admin_dashboard.html')

@login_required
def nurse(request):
    return render(request, 'nurse_dashboard.html')

