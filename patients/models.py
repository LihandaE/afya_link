from django.db import models


class PatientProfile(models.Model):

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )

    national_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}"
    