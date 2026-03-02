from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import PatientProfile
from .serializers import *


class PatientProfileViewSet(viewsets.ModelViewSet):

    queryset = PatientProfile.objects.all()
    serializer_class = PatientRegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Patient sees only their profile
        if user.role == "patient":
            return PatientProfile.objects.filter(user=user)

        # Hospital staff see patients linked to their hospital visits
        return PatientProfile.objects.all()

