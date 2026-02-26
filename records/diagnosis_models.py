from django.db import models


class Diagnosis(models.Model):

    visit = models.ForeignKey(
        "patients.Visit",
        on_delete=models.CASCADE,
        related_name="diagnoses"
    )

    doctor = models.ForeignKey(
        "doctors.Doctor",
        on_delete=models.SET_NULL,
        null=True
    )

    patient_history = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis - {self.visit}"