from django.db import models
from django.conf import settings

# Create your models here.

class Speciality(models.Model):
    name =models.CharField(max_length=260, unique=True)

    def __str__(self):
        return self.name
    
class Doctor(models.Model):
    doctor_profile =models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialities= models.ManyToManyField(Speciality)
    hospitals= models.ManyToManyField('hospitals.Hospital')

    license_number = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr.{self.doctor_profile.first_name}"