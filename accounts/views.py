from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import User
from .serializers import UserSerializer


# USER MANAGEMENT


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

        # HOSPITAL ADMIN CAN CREATE STAFF
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

# LOGIN VIEW


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(email=email, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {"error": "Account disabled"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
                "hospital": user.hospital.id if user.hospital else None,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )