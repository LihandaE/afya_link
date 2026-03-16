# visits/serializers.py

from rest_framework import serializers
from .models import Visit


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = "__all__"
        read_only_fields = ["status", "completed_at"]

    def validate(self, attrs):
        user = self.context["request"].user

        # Hospital staff can only create visits in their hospital
        if user.role != "super_admin":
            if attrs["hospital"] != user.hospital:
                raise serializers.ValidationError(
                    {"error": "Cannot create visit outside your hospital"}
                )

        return attrs