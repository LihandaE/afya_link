"""
records/models.py

This file aggregates all record-related models so that
Django can properly register them under the `records` app.
"""

from .lab_models import LabRecord
from .radiology_models import RadiologyRecord
from .diagnosis_models import Diagnosis
from .prescription_models import Prescription

# Optional: Explicit export (cleaner for large systems)
__all__ = [
    "LabRecord",
    "RadiologyRecord",
    "Diagnosis",
    "Prescription",
]