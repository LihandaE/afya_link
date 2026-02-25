from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, Speciality
from .serializers import DoctorSerializer, SpecialitySerializer


class SpecialityViewset(viewsets.ModelViewSet):
    queryset= Speciality.objects.all()
    serializer_class= SpecialitySerializer
    permission_classes= [IsAuthenticated]

class DoctorViewset( viewsets.ModelViewSet):
    queryset= Doctor.objects.all()
    serializer_class= DoctorSerializer
    permission_classes=[IsAuthenticated]

    