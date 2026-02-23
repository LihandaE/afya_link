from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils import timezone



# USER MANAGER


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'super_admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)



# CUSTOM USER MODEL (AUTH LAYER)


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('hospital_admin', 'Hospital Admin'),
        ('doctor', 'Doctor'),
        ('consultant', 'Consultant'),
        ('nurse', 'Nurse'),
        ('lab_tech', 'Lab Technologist'),
        ('radiologist', 'Radiologist'),
        ('pharmacist', 'Pharmacist'),
        ('receptionist', 'Receptionist'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.role}"



# HOSPITAL


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# SPECIALITY


class Speciality(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



# DOCTOR PROFILE (PROFESSIONAL LAYER)


class Doctor(models.Model):

    doctor_profile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role__in': ['doctor', 'consultant']},
        related_name='doctor_profile'
    )

    specialities = models.ManyToManyField(
        Speciality,
        related_name='doctors'
    )

    hospitals = models.ManyToManyField(
        Hospital,
        related_name='doctors'
    )

    license_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)

    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.doctor_profile.first_name} {self.doctor_profile.last_name}"



# DOCTOR AVAILABILITY


class DoctorAvailability(models.Model):

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='availabilities'
    )

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )

    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.day_of_week}"
    
def is_doctor_available(doctor, hospital, date, time):

    day_name = date.strftime('%A')

    available = DoctorAvailability.objects.filter(
        doctor=doctor,
        hospital=hospital,
        day_of_week=day_name,
        start_time__lte=time,
        end_time__gte=time,
        is_available=True
    ).exists()

    if not available:
        return False

    conflict = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=date,
        appointment_time=time,
        status='scheduled'
    ).exists()

    return not conflict


# PATIENT


class Patient(models.Model):
    national_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# VISIT


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.hospital}"



# APPOINTMENT


class Appointment(models.Model):

    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.appointment_date}"



# LAB RECORD


class LabRecord(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='lab_records')
    lab_tech = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    report_image = CloudinaryField('lab_report', folder='afyalink/labs')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# RADIOLOGY RECORD


class RadiologyRecord(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='radiology_records')
    radiologist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    scan_image = CloudinaryField('radiology_scan', folder='afyalink/radiology')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# DIAGNOSIS


class Diagnosis(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='diagnoses')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)

    patient_history = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



# PRESCRIPTION


class Prescription(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='prescriptions')
    pharmacist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


# ACCESS CONSENT (OTP)


class AccessConsent(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    requesting_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.expires_at


# AUDIT LOG


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

