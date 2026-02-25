from rest_framework import serializers
from .models import Doctor, Speciality

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model= Speciality
        fields= '__all__'

class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model= Doctor
        fields= '__all__'
        