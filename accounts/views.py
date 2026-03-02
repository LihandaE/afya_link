from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer
from accounts.permissions import *


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):

        user = self.request.user

        if user.role == "super_admin":
            return User.objects.all()

        if user.role == "hospital_admin":
            return User.objects.filter(hospital=user.hospital)

        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):

        creator = self.request.user
        role = serializer.validated_data.get("role")

        # SUPER ADMIN CAN CREATE ANYONE
        if creator.role == "super_admin":
            serializer.save()
            return

        # HOSPITAL ADMIN CAN CREATE STAFF ONLY FOR OWN HOSPITAL
        if creator.role == "hospital_admin":

            if role in [
                "doctor",
                "consultant",
                "nurse",
                "lab_tech",
                "radiologist",
                "pharmacist",
                "receptionist",
            ]:
                serializer.save(hospital=creator.hospital)
                return

        raise PermissionError("You cannot create this user.")
    
