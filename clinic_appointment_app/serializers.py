from rest_framework import serializers
from .models import User, DoctorProfile, Appointment


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

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


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
