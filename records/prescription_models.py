from django.db import models


class Prescription(models.Model):

    visit = models.ForeignKey(
        "patients.Visit",
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )

    pharmacist = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={"role": "pharmacist"}
    )

    medication_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication_name} - {self.visit}"