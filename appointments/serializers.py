from rest_framework import serializers
from .models import Appointment
from doctors.services import assign_doctor


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model= Appointment
        fields = '__all__'
        read_only_fields =['doctor']

    def create(self, validated_data):
        
        hospital= validated_data['hospital']
        speciality= validated_data['speciality']
        date= validated_data['appointment_date']
        time= validated_data['appointment_time']

        doctor= assign_doctor(hospital, speciality, date, time)

        if not doctor:
            raise serializers.ValidationError( 
                {"error": 'No doctor available for the selected time slot'}
            )
        
        validated_data['doctor'] = doctor

        return super().create(validated_data)
        