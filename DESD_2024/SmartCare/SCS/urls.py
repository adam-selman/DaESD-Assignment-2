from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
   path('', views.Auth, name='auth'),
   path('login', views.Login, name='login'),
   path('reset_password', views.password_reset, name='resetPassword'),
   path('nurse_dashboard', views.nurse, name='nursDash'),
   path('doctor_dashboard', views.doc, name='docDash'),
   path('patient_dashboard', views.patient, name='patDash'),
   path('admin_dashboard', views.admin, name='admDash'),
   path('logout',views.Logout),
   path('check_status',views.check_session),
   path('Session_status',views.Session),
]