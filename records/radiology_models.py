from django.db import models
from cloudinary.models import CloudinaryField


class RadiologyRecord(models.Model):
    visit=models.ForeignKey(
        'patients.Visit',
        on_delete=models.CASCADE,
        related_name='radiology_records'
    )

    radiologist=models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'radiologist'}
    )

    scan_type=models.CharField(max_length=280)

    image_file= CloudinaryField(
        'radilogy_scan',
        folder='afyalink/radiology'
    )

    notes=models.TextField(blank=True, null=True)

    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.scan_type} - {self.visit}"