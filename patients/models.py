from django.db import models

# Create your models here.

class Patient(models.Model):
    national_id =models.CharField(max_length=50, unique=True)
    first_name= models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    date_of_birth=models.DateField()
    phone_number=models.CharField(max_length=20)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    