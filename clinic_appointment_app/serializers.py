from rest_framework import serializers
from .models import User, DoctorProfile, Appointment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'id', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["user"] = {
            'id': self.user.id,
            "email": self.user.email,
            "role": self.user.role,
            "full_name": self.user.full_name
        }

        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'full_name', 'email', 'specialization',
                  'available_from', 'available_to']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(
        source='doctor.user.full_name', read_only=True)
    patient_name = serializers.CharField(
        source='patient.full_name', read_only=True)
    # role = serializers.CharField(source='patient.role', read_only=True)
    patient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='PATIENT'))

    class Meta:
        model = Appointment
        fields = ['id', 'doctor_name', 'doctor',
                  'patient_name', 'patient', 'date', 'time', 'status']
