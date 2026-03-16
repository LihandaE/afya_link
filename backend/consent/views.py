from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
import random
from consent.serializers import AccessConsentSerializer
from .models import AccessConsent


class ConsentViewSet(viewsets.ModelViewSet):

    queryset = AccessConsent.objects.all()
    serializer_class = AccessConsentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def request_otp(self, request, pk=None):

        consent = self.get_object()

        otp = str(random.randint(100000, 999999))
        consent.otp = otp
        consent.expires_at = timezone.now() + timedelta(minutes=5)
        consent.save()

        return Response({"message": "OTP sent"})

    @action(detail=True, methods=["post"])
    def verify_otp(self, request, pk=None):

        consent = self.get_object()
        otp_input = request.data.get("otp")

        if consent.otp != otp_input or consent.is_expired():
            return Response({"error": "Invalid or expired OTP"})

        consent.is_verified = True
        consent.save()

        return Response({"message": "Access granted"})
