from .models import Doctor
from appointments.models import Appointment


def is_doctor_available(doctor, hospital, date, time):

    conflict= Appointment.objects.filter(
        doctor=doctor,
        hospital=hospital,
        appointment_date=date,
        appointment_time=time,
        status='scheduled'
    ) .exists()

    return not conflict

def assign_doctor(hospital, speciality, date, time):

    doctors= Doctor.objects.filter(
        hospitals=hospital,
        specialities=speciality,
        is_active= True
    )

    for doctor in doctors:
        if is_doctor_available(doctor, hospital, date, time):
            return doctor
        
    return None
