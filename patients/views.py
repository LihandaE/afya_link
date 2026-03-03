from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import PatientProfile
from .serializers import *


class PatientProfileViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Patient sees only their own profile
        if user.role == "patient":
            return PatientProfile.objects.filter(user=user)

        # Hospital staff / admins
        return PatientProfile.objects.all()


    def get_serializer_class(self):
        if self.action == "create":
            return PatientRegistrationSerializer
        return PatientProfileSerializer

    
    def perform_update(self, serializer):
        user = self.request.user
        instance = self.get_object()

        # Prevent patient from editing someone else's record
        if user.role == "patient" and instance.user != user:
            raise PermissionDenied("You cannot modify another patient's profile.")

        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user

        # Patients should not delete profiles
        if user.role == "patient":
            raise PermissionDenied("Patients cannot delete their profile.")

        instance.delete()