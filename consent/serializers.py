from rest_framework import serializers
from .models import AccessConsent


class AccessConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessConsent
        fields = "__all__"
        read_only_fields = ["is_verified"]