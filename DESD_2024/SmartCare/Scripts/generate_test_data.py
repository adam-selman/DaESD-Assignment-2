
doctors = []
patients = []
appointments = []
nurses = []

def generate_appointments():
    # Generate appointments
    appointments = []
    for i in range(10):
        appointment = {
            'id': i,
            'date': '2021-09-01',
            'time': '10:00',
            'patient_id': i,
            'doctor_id': i
        }
        appointments.append(appointment)
    return appointments
