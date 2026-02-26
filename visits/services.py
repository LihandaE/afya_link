# visits/services.py

from .models import Visit


def create_visit(patient, hospital, user, appointment=None, reason=None):

    return Visit.objects.create(
        patient=patient,
        hospital=hospital,
        created_by=user,
        appointment=appointment,
        reason_for_visit=reason
    )