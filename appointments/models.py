from django.db import models

# Create your models here.

class Appointment(models.Model):

    STATUS_CHOICES =(
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),

    )
    patient= models.ForeignKey('patients.PatientProfile', on_delete=models.CASCADE)
    hospital= models.ForeignKey('hospitals.Hospital', on_delete=models.CASCADE)
    speciality= models.ForeignKey('doctors.Speciality', on_delete=models.SET_NULL, null=True)
    doctor= models.ForeignKey('doctors.Doctor', on_delete=models.SET_NULL,null=True)

    appointment_date= models.DateTimeField()
    appointment_time= models.TimeField()
    status=models.CharField(max_length=25, choices=STATUS_CHOICES, default='scheduled')

    created_at= models.DateTimeField(auto_now_add=True)

    