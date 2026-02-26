from django.db import models
from cloudinary.models import CloudinaryField


class LabRecord(models.Model):

    visit= models.ForeignKey(
        'patients.Visit',
        on_delete=models.CASCADE,
        related_name='lab_records'
    )

    lab_tech= models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'lab_tech'}
    )

    test_name= models.CharField(max_length=260)

    report_file= CloudinaryField(
        'lab_report', 
        folder='afyalink/labs')
    
    notes= models.TextField(blank=True, null=True)

    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} - {self.visit}"