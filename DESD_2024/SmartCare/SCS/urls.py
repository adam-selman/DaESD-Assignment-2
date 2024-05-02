from django.urls import path
from . import views


urlpatterns = [
   path('', views.Auth, name='auth'),
   path('login/', views.Login, name='login'),  #fixes for login path includes the needed /
   path('dashboard', views.dashboard_resolver, name='dashboard'),
   path('patient_appointment_booking', views.patient_appointment_booking, name='patientBooking'),
   path('retrieve_practitioners_by_day_and_service', views.retrieve_practitioners_by_day_and_service),
   path('retrieve_time_slots_by_day_and_practitioner', views.retrieve_time_slots_by_day_and_practitioner),
   path('logout',views.Logout),
   path('check_status',views.check_session),
   path('Session_status',views.Session),
   path('generate_invoice/',views.generate_invoice),
   path('generate_patient_forwarding_file',views.generate_patient_forwarding_file),
   path('register/', views.register, name='register'),
   path('staff_register/', views.register_doctor_nurse, name='staff_register'),
   path('Auth/', views.Auth, name='Auth'),
   path('DisplayPatients',views.display_patients),
   path('DisplayAppt',views.currentAppt),
   path('delete/<int:id>/',views.delete_patient),
   path('Delete/<int:id>/',views.delete_appointment),
   path('ADM_Delete/<int:id>/',views.ADM_delete_appointment),
   path('update-patient/',views.update_patient),
   path('filter-patient/',views.filter_patient),
   path('filter-appointments/',views.filter_appointments),
   path('DisplayHistoricAppointments',views.historic_appointments),
   path('DisplayPendingPrescriptions',views.prescription_approval),
   path('DisplayPrescriptions',views.historic_prescriptions),
   path('approve_prescription',views.approve_prescription),
   path('mark_invoice_as_paid',views.mark_invoice_as_paid),
   path('request_repeat_prescription', views.request_repeat_prescription, name='requestRepeatPrescription'), 
   path('update_doctor_service_rate', views.update_doctor_service_rate, name='updateDoctorServiceRate'),
   path('update_nurse_service_rate', views.update_nurse_service_rate, name='updateNurseServiceRate'),
   path('generate_report', views.generate_report, name='generateReport'),
   path('complete_appointment', views.complete_appointment, name='completeAppointment'),
   path('start_appointment', views.start_appointment, name='startAppointment'),
   path('make_payment', views.make_payment, name='make_payment'),
]