from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from appointment.models import Appointment
from appointment.AppointmentSerializer import AppointmentSerializer
from demo.models import CallNotification,Order
from demo.serializers.call_serializers import CallNotificationSerializer
from demo.serializers.canteen_serializers import GetOrderSerializer



@receiver(post_save, sender=Appointment)
def update_index_page(sender, instance, **kwargs):
    """Send only relevant updates to WebSocket group"""
    channel_layer = get_channel_layer()

    # Serialize the updated appointment
    serialized_data = AppointmentSerializer(instance).data
    # Send the updated appointment data to the WebSocket group
    async_to_sync(channel_layer.group_send)(
    'index_page',  
    {
        'type': 'update_index_page',  # Must match exactly
        'data': serialized_data
    }
    
    )







@receiver(post_save, sender=CallNotification)
def call_notify(sender, instance, **kwargs):
    """Send only relevant updates (Today's & Pending) to WebSocket group"""
    channel_layer = get_channel_layer()
    
    # Check if the instance is today's and has status 'pending'
    if instance.read == False:
        # Serialize the filtered instance
        serialized_data = CallNotificationSerializer(instance).data
        async_to_sync(channel_layer.group_send)(
            'call_live',  
            {
                'type': 'call_notify',
                'data': serialized_data  # Sending only filtered data
            }
        )




@receiver(post_save, sender=Order)
def order_notify(sender, instance, **kwargs):
    """Send only relevant updates (Today's & Pending) to WebSocket group"""
    channel_layer = get_channel_layer()
    
    # Check if the instance is today's and has status 'pending'
    if instance.status == False:
        # Serialize the filtered instance
        serialized_data = GetOrderSerializer(instance).data

        async_to_sync(channel_layer.group_send)(
            'order_live',  
            {
                'type': 'order_notify',
                'data': serialized_data  # Sending only filtered data
            }
        )