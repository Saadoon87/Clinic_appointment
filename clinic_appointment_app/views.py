from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import datetime
import jwt
from .utils import AuthenticateUser
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from rest_framework.exceptions import AuthenticationFailed


# Create your views here.
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewUsersAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        print(user_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect User"})

        # Permissions or Authorizations
        if user.role not in ["DOCTOR", "ADMIN"]:
            return Response({"detail": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        print(user_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect User"}, status=status.HTTP_401_UNAUTHORIZED)

        doctors = DoctorProfile.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        print(user_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect User"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role not in ["ADMIN", "DOCTOR"]:
            return Response({"detail": "You dont have permission"})

        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_id = request.user.id
        print(user_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect User"}, status=status.HTTP_401_UNAUTHORIZED)

        if user.role != "PATIENT":
            return Response({"detail": "You dont have permission"})

        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        user_id = request.user.id
        print(user_id)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Incorrect User"}, status=status.HTTP_401_UNAUTHORIZED)

        appointment = Appointment.objects.get(pk=pk)
        serializer = AppointmentSerializer(appointment, data=request.data)

        if serializer.is_valid():
            if user.id == appointment.patient.id or user.id == appointment.doctor.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "You cannot edit this appointment"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
