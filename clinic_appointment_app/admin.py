from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(DoctorProfile)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'specialization']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'role']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'patient',
                    'date', 'start_time', 'end_time', 'status']
