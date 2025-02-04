from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from appointment.models import Appointment
from appointment.AppointmentSerializer import AppointmentSerializer

@receiver(post_save, sender=Appointment)
def update_index_page(sender, instance, **kwargs):
    """Send only relevant updates to WebSocket group"""
    channel_layer = get_channel_layer()

    # Serialize the updated appointment
    serialized_data = AppointmentSerializer(instance).data
    # print(serialized_data)
    # Send the updated appointment data to the WebSocket group
    async_to_sync(channel_layer.group_send)(
        'index_page',  
        {
            'type': 'update_index_page',
            'data': serialized_data  # Sending only updated appointment
        }
    )
