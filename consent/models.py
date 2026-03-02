# Create your models here.
from django.db import models
from django.utils import timezone


class AccessConsent(models.Model):
    patient = models.ForeignKey("patients.PatientProfile", on_delete=models.CASCADE)
    requesting_hospital = models.ForeignKey("hospitals.Hospital", on_delete=models.CASCADE)

    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.expires_at