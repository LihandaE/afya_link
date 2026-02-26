from rest_framework import serializers
from .lab_models import LabRecord
from .radiology_models import RadiologyRecord
from .diagnosis_models import Diagnosis
from .prescription_models import Prescription


class LabRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabRecord
        fields = "__all__"


class RadiologyRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadiologyRecord
        fields = "__all__"


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = "__all__"


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"