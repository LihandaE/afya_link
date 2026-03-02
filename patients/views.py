from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PatientRegistrationSerializer


class PatientRegisterView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = PatientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient registered successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

