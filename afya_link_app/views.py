from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from datetime import datetime, timedelta
import random
from .models import *


# DASHBOARD

@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# REGISTER PATIENT

@login_required
def register_patient(request):
    if request.method == "POST":
        national_id = request.POST.get("national_id")

        patient, created = Patient.objects.get_or_create(
            national_id=national_id,
            defaults={
                "first_name": request.POST.get("first_name"),
                "last_name": request.POST.get("last_name"),
                "date_of_birth": request.POST.get("date_of_birth"),
                "phone_number": request.POST.get("phone_number"),
            }
        )

        return JsonResponse({
            "message": "Patient registered",
            "created": created
        })

    return render(request, "patients/register.html")


# CREATE VISIT

@login_required
def create_visit(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    # In real deployment, use request.user hospital logic
    hospital = Hospital.objects.first()

    visit = Visit.objects.create(
        patient=patient,
        hospital=hospital,
        created_by=request.user
    )

    AuditLog.objects.create(
        user=request.user,
        patient=patient,
        action="Created Visit"
    )

    return JsonResponse({
        "message": "Visit created",
        "visit_id": visit.id
    })


# BOOK APPOINTMENT (AUTO DOCTOR ASSIGNMENT)

@login_required
@transaction.atomic
def book_appointment(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == "POST":

        hospital_id = request.POST.get("hospital")
        speciality_id = request.POST.get("speciality")
        date = request.POST.get("date")
        time = request.POST.get("time")

        hospital = Hospital.objects.get(id=hospital_id)
        speciality = Speciality.objects.get(id=speciality_id)

        appointment_date = datetime.strptime(date, "%Y-%m-%d").date()
        appointment_time = datetime.strptime(time, "%H:%M").time()

        doctors = Doctor.objects.filter(
            hospitals=hospital,
            specialities=speciality,
            is_active=True
        )

        assigned_doctor = None

        for doctor in doctors:
            if is_doctor_available(doctor, hospital, appointment_date, appointment_time):
                assigned_doctor = doctor
                break

        if not assigned_doctor:
            return JsonResponse(
                {"error": "No available doctor"},
                status=400
            )

        appointment = Appointment.objects.create(
            patient=patient,
            hospital=hospital,
            speciality=speciality,
            doctor=assigned_doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        AuditLog.objects.create(
            user=request.user,
            patient=patient,
            action="Booked Appointment"
        )

        return JsonResponse({
            "message": "Appointment booked",
            "doctor": str(assigned_doctor),
            "appointment_id": appointment.id
        })

    return render(request, "appointments/book.html")


# REQUEST OTP CONSENT

@login_required
def request_access_consent(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)
    hospital = Hospital.objects.first()

    otp = str(random.randint(100000, 999999))
    expiry = timezone.now() + timedelta(minutes=5)

    AccessConsent.objects.create(
        patient=patient,
        requesting_hospital=hospital,
        otp=otp,
        expires_at=expiry
    )

    # In production: integrate SMS API here
    print("Generated OTP:", otp)

    return JsonResponse({"message": "OTP sent"})



# VERIFY OTP

@login_required
def verify_otp(request, patient_id):

    if request.method == "POST":

        otp_input = request.POST.get("otp")

        consent = AccessConsent.objects.filter(
            patient_id=patient_id,
            otp=otp_input,
            is_verified=False
        ).first()

        if not consent:
            return JsonResponse(
                {"error": "Invalid OTP"},
                status=400
            )

        if consent.is_expired():
            return JsonResponse(
                {"error": "OTP expired"},
                status=400
            )

        consent.is_verified = True
        consent.save()

        return JsonResponse({"message": "Access granted"})

    return render(request, "otp/verify.html")



# VIEW PATIENT RECORDS (READ ONLY)

@login_required
def view_patient_records(request, patient_id):

    patient = get_object_or_404(Patient, id=patient_id)

    visits = patient.visits.all()
    diagnoses = Diagnosis.objects.filter(visit__patient=patient)
    prescriptions = Prescription.objects.filter(visit__patient=patient)
    labs = LabRecord.objects.filter(visit__patient=patient)
    radiology = RadiologyRecord.objects.filter(visit__patient=patient)

    return render(request, "patients/records.html", {
        "patient": patient,
        "visits": visits,
        "diagnoses": diagnoses,
        "prescriptions": prescriptions,
        "labs": labs,
        "radiology": radiology,
    })


# ADD DIAGNOSIS

@login_required
def add_diagnosis(request, visit_id):

    visit = get_object_or_404(Visit, id=visit_id)

    if request.method == "POST":

        if not hasattr(request.user, "doctor_profile"):
            return JsonResponse(
                {"error": "Only doctors can add diagnosis"},
                status=403
            )

        Diagnosis.objects.create(
            visit=visit,
            doctor=request.user.doctor_profile,
            patient_history=request.POST.get("history"),
            diagnosis=request.POST.get("diagnosis"),
            treatment_plan=request.POST.get("treatment")
        )

        AuditLog.objects.create(
            user=request.user,
            patient=visit.patient,
            action="Added Diagnosis"
        )

        return JsonResponse({"message": "Diagnosis added"})

    return render(request, "diagnosis/add.html")