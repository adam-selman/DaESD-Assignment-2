from django.urls import path
from . import views


urlpatterns = [
   path('', views.Auth, name='auth'),
   path('login/', views.Login, name='login'),  #fixes for login path includes the needed /
   path('nurse_dashboard', views.nurse, name='nursDash'),
   path('doctor_dashboard', views.doc, name='docDash'),
   path('patient_dashboard', views.patient, name='patDash'),
   path('admin_dashboard/', views.admin_dash, name='admin_dash'),
   path('patient_appointment_booking', views.patient_appointment_booking, name='patientBooking'),
   path('retrieve_practitioners_by_day_and_service', views.retrieve_practitioners_by_day_and_service, name='getPractitionersByDayAndService'),
   path('retrieve_time_slots_by_day_and_practitioner', views.retrieve_time_slots_by_day_and_practitioner, name='getPractitionersByDayAndService'),
   path('logout',views.Logout),
   path('check_status',views.check_session),
   path('Session_status',views.Session),
   path('generate_invoice',views.generate_invoice),
   path('register/', views.register, name='register'),
   path('staff_register/', views.register_doctor_nurse, name='staff_register'),
   path('Auth/', views.Auth, name='Auth'),
   path('DisplayPatients',views.display_patients),
   path('DisplayAppt',views.currentAppt),
   path('delete/<int:id>/',views.delete_patient),
   path('Delete/<int:id>/',views.delete_appointment),
   path('update-patient/',views.update_patient),
   path('DisplayHistoricAppointments',views.historic_appointments),
   path('DisplayPendingPrescriptions',views.prescription_approval),
   path('DisplayPrescriptions',views.historic_prescriptions),
   path('approve_prescription',views.approve_prescription),
   path('mark_invoice_as_paid',views.mark_invoice_as_paid),
   path('request_repeat_prescription', views.request_repeat_prescription, name='requestRepeatPrescription'), 
   path('update_doctor_service_rate', views.update_doctor_service_rate, name='updateDoctorServiceRate'),
   path('update_nurse_service_rate', views.update_nurse_service_rate, name='updateNurseServiceRate'),
   path('password_reset', views.password_reset, name='password_reset'),
   path('password_reset_change/', views.password_reset_change, name='password_reset_change'),
   path('password_reset_done', views.password_reset_done, name='password_reset_done')
]