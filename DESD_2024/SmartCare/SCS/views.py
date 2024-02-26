from django.shortcuts import render,redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'index.html')


#can change anything here based on our other implementation 
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'accounts/login.html')
