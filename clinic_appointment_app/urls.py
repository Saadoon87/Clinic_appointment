from django.urls import path
from .views import *


urlpatterns = [
    path('api/auth/register/', RegisterAPIView.as_view(), name='register'),
    path('api/users/', ViewUsersAPIView.as_view(), name='view_all'),
    path('api/doctors/', DoctorAPIView.as_view(), name='doctors'),
    path('api/appointments/', AppointmentAPIView.as_view(), name='appointments'),
    path('api/appointments/<int:pk>/',
         AppointmentAPIView.as_view(), name='update_appointments'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
