from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewset(viewsets.ModelViewSet):

    serializer_class= AppointmentSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        
        user= self.request.user

        if user.role == 'super_admin':
            return Appointment.objects.all()
        if user.role in ['doctor', 'consultant']:
            return Appointment.objects.filter(
                doctor__doctor_profile=user
            )
        return Appointment.objects.filter(
            hospital=user.hospital
        )