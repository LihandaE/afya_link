from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Patient
from .serializers import PatientSerializer
from accounts.permissions import *


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    permission_classes = [IsReceptionist | IsHospitalAdmin | IsSuperAdmin]

    def get_queryset(self):
        if self.request.user.role == "super_admin":
            return Patient.objects.all()
        return Patient.objects.filter(visits__hospital=self.request.user.hospital)

