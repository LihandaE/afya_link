from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        # Super admin sees everyone
        if user.role == "super_admin":
            return User.objects.all()

        # Hospital admin sees only their hospital staff
        if user.role == "hospital_admin":
            return User.objects.filter(hospital=user.hospital)

        # Normal users only see themselves
        return User.objects.filter(id=user.id)

    def perform_create(self, serializer):

        creator = self.request.user
        role = serializer.validated_data.get("role")

        # SUPER ADMIN CAN CREATE ANYONE
        if creator.role == "super_admin":
            serializer.save()
            return

        # HOSPITAL ADMIN CAN CREATE STAFF FOR THEIR HOSPITAL
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

            raise PermissionDenied("Hospital admin cannot create this role.")

        # Everyone else cannot create users
        raise PermissionDenied("You do not have permission to create users.")