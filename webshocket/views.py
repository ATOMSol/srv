from django.shortcuts import render
from rest_framework.response import Response

from appointment.models import Appointment
from appointment.Serializers import AppointmentSerializer


def index(request):
    appointments = Appointment.objects.all()
    return render(request, 'i.html', {'appointments': appointments})


# Create your views here.
def ws_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'i.html', {'appointments': appointments})

    # data=Appointment.objects.all()
    # print(data)
    # serial=AppointmentSerializer.AppointmentSerializer(data, many=True)
    # print({'RES' : serial.data})
    # return Response({'RES': serial.data})

def chat_view(request):
    return render(request, 'chat.html')