from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    LabRecordSerializer,
    RadiologyRecordSerializer,
    DiagnosisSerializer,
    PrescriptionSerializer
)
from .lab_models import LabRecord
from .radiology_models import RadiologyRecord
from .diagnosis_models import Diagnosis
from .prescription_models import Prescription
from accounts.permissions import*


class LabRecordViewSet(viewsets.ModelViewSet):
    queryset = LabRecord.objects.all()
    serializer_class = LabRecordSerializer
    permission_classes = [IsAuthenticated | IsLabTech | IsDoctor | IsSuperAdmin]


class RadiologyRecordViewSet(viewsets.ModelViewSet):
    queryset = RadiologyRecord.objects.all()
    serializer_class = RadiologyRecordSerializer
    permission_classes = [IsAuthenticated | IsRadiologist | IsSuperAdmin]


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated | IsDoctor | IsSuperAdmin]


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated | IsPharmacist | IsSuperAdmin]