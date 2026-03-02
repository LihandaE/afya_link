from rest_framework import serializers
from accounts.models import  *
from patients.models import PatientProfile


class PatientRegistrationSerializer(serializers.ModelSerializer):

    national_id = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
            "national_id",
            "phone_number",
            "date_of_birth",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        national_id = validated_data.pop("national_id")
        phone_number = validated_data.pop("phone_number")
        date_of_birth = validated_data.pop("date_of_birth")

        user = User.objects.create_user(
            role="patient",
            **validated_data
        )

        PatientProfile.objects.create(
            user=user,
            national_id=national_id,
            phone_number=phone_number,
            date_of_birth=date_of_birth
        )

        return user