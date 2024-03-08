from django.urls import path
from . import views


urlpatterns = [
   path('', views.Auth, name='auth'),
   path('login', views.Login, name='login'),
   path('nurse_dashboard', views.nurse, name='nursDash'),
   path('doctor_dashboard', views.doc, name='docDash'),
   path('patient_dashboard', views.patient, name='patDash'),
   path('admin_dashboard', views.admin, name='admDash'),
   path('patient_appointment_booking', views.patient_appointment_booking, name='patientBooking'),
   path('get_practitioners_by_day_and_service', views.get_practitioners_by_day_and_service, name='getPractitionersByDayAndService'),
   path('get_time_slots_by_day_and_practitioner', views.get_time_slots_by_day_and_practitioner, name='getPractitionersByDayAndService'),
   path('logout',views.Logout),
   path('check_status',views.check_session),
   path('Session_status',views.Session),
   path('register/', views.register, name='register'),
   path('staff_register/', views.register_doctor_nurse, name='staff_register'),
]