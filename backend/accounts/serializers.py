from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


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

class LoginSerializer(serializers.Serializer):
     email= serializers.EmailField()
     password= serializers.CharField(write_only=True)

     def validate(self, data):
        
        email=data.get('email')
        password=data.get('password')

        user=authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('User account is disabled')
        data['user']=user
        return data
         