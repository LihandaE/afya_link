from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Hospital
from .serializers import HospitalSerializer
from accounts.permissions import *


class HospitalViewSet(viewsets.ModelViewSet):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [IsAuthenticated | IsSuperAdmin | IsHospitalAdmin ]

    
