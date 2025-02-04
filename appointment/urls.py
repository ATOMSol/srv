
from django.urls import path,include
# from .views import AppointmentCreateView
# from .views import AppointmentCreateAPIView,AppointmentDetailAPIView

urlpatterns = [
    path('appointments/', include('appointment.appointment_urls')),

]