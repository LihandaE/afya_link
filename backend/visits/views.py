# visits/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Visit
from .serializers import VisitSerializer
from accounts.permissions import IsHospitalStaff


class VisitViewSet(viewsets.ModelViewSet):

    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated, IsHospitalStaff]

    def get_queryset(self):

        user = self.request.user

        if user.role == "super_admin":
            return Visit.objects.all()

        if user.role in ["doctor", "consultant"]:
            return Visit.objects.filter(
                hospital=user.hospital
            )

        return Visit.objects.filter(
            hospital=user.hospital
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)