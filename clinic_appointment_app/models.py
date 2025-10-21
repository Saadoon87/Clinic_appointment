from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please add email !!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", "ADMIN")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        DOCTOR = "DOCTOR", "doctor"
        PATIENT = "PATIENT", "patient"
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(choices=Roles.choices,
                            max_length=10, default=Roles.PATIENT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.full_name} - {self.role}"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    available_from = models.TimeField()
    available_to = models.TimeField()

    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.specialization}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "pending"
        CONFIRMED = "CONFIRMED", "confirmed"
        COMPLETED = "COMPLETED", "completed"
        CANCELLED = "CANCELLED", "cancelled"

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=Status.choices,
                              max_length=10, default=Status.PENDING)

    def __str__(self):
        return f"Appointment with {self.doctor.user.full_name} on {self.date} at {self.time}"
