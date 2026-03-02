from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer



class UserViewSet(viewsets.ModelViewSet):

    serializer_class= UserSerializer
    permission_classes= [AllowAny]

    def get_queryset(self):
        user= self.request.user
        if user.role =='super_admin':
            return User.objects.all()
        return User.objects.filter(hospital=user.hospital)
    
