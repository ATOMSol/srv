
from django.urls import path,include
from appointment.views import AppointmentCreateView,AppointmentListView,AppointmentUpdateView,DeleteAppointmentView
from rest_framework.routers import SimpleRouter

appointment = SimpleRouter()
appointment.register(r'create-appointments', AppointmentCreateView, basename='create-appointments')
appointment.register(r'get-appointments', AppointmentListView, basename='get-appointments')
appointment.register(r'update-appointments', AppointmentUpdateView, basename='update-appointments')
appointment.register(r'delete-appointments', DeleteAppointmentView, basename='delete-appointments')

# urlpatterns = [
#     path('create-appointments/',AppointmentCreateView, name='create-appointment'),
#     path('get-appointments/',AppointmentListView, name='get-appointments'),
#     path('update-appointments/',AppointmentUpdateView, name='update-appointments'),
#     path('delete-appointments/', DeleteAppointmentView, name='delete_appointment'),
# ]

urlpatterns = appointment.urls
#     path('', include(appointment.urls)),
# ]