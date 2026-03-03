from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["is_staff", "is_superuser"]

def create(self, validated_data):
    groups = validated_data.pop('groups', [])
    password = validated_data.pop('password')

    user = User.objects.create(**validated_data)
    user.set_password(password)
    user.save()

    if groups:
        user.groups.set(groups)

    return user