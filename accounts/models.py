from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "super_admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("superadmin", "Super Admin"),
        ("hospitaladmin", "Hospital Admin"),
        ("doctor", "Doctor"),
        ("consultant", "Consultant"),
        ("nurse", "Nurse"),
        ("labtech", "Lab Tech"),
        ("radiologist", "Radiologist"),
        ("pharmacist", "Pharmacist"),
        ("receptionist", "Receptionist"),
        ("patient", "Patient"),
    )

    email = models.EmailField(unique=True, blank=False, null=False)
    username= None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="patient")

    hospital = models.ForeignKey(
        "hospitals.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="staff"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    def is_doctor(self):
        return self.role in ['doctor', 'consultant']
    def is_nurse(self):
        return self.role == 'nurse'
    def is_pharmacist(self):
        return self.role == 'pharmacist'
    def is_lab_tech(self):
        return self.role == 'labtech'
    def is_radiologist(self):
        return self.role == 'radiologist'
    def is_hospital_admin(self):
        return self.role in ['superadmin', 'hospitaladmin']
    def is_receptionist(self):
        return self.role == 'receptionist'
    def is_patient(self):
        return self.role == 'patient'
    def is_super_admin(self):
        return self.role == 'superadmin'
    