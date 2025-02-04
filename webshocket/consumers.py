import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from appointment.models import Appointment
from appointment.Serializers.AppointmentSerializer import AppointmentSerializer
from webshocket.models import Message

logger = logging.getLogger(__name__)

class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("WebSocket connect attempt from %s", self.scope["client"])
        try:
            # Join the appointments group
            await self.channel_layer.group_add("appointments", self.channel_name)
            await self.accept()
            
            # Send initial data
            try:
                initial_data = await self.get_initial_data()
                await self.send(text_data=json.dumps({
                    'type': 'initial_data',
                    'data': initial_data
                }))
                logger.info("Initial data sent successfully")
            except Exception as e:
                logger.error(f"Error getting initial data: {str(e)}")
                raise
                
            logger.info("WebSocket connection established successfully")
            
        except Exception as e:
            logger.error(f"Error in connect: {str(e)}", exc_info=True)
            raise

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("appointments", self.channel_name)
            logger.info(f"WebSocket disconnected with code: {close_code}")
        except Exception as e:
            logger.error(f"Error in disconnect: {str(e)}")

    async def appointment_update(self, event):
        """
        Handle appointment updates and send to WebSocket
        """
        try:
            if 'data' in event:
                await self.send(text_data=json.dumps({
                    'type': 'appointment_update',
                    'data': event['data']
                }))
                logger.info("Update sent to client")
            else:
                logger.error("Invalid event data")
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")

    @database_sync_to_async
    def get_initial_data(self):
        """
        Get all appointments for initial data load
        """
        try:
            data = Appointment.objects.all()
            serializer = AppointmentSerializer(data, many=True)
            return serializer.data
        except Exception as e:
            logger.error(f"Error in get_initial_data: {str(e)}")
            raise

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Join the chat group
            await self.channel_layer.group_add("chat_room", self.channel_name)
            await self.accept()
            logger.info("Chat WebSocket connected")
        except Exception as e:
            logger.error(f"Error in chat connect: {str(e)}")
            raise

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard("chat_room", self.channel_name)
            logger.info(f"Chat WebSocket disconnected with code: {close_code}")
        except Exception as e:
            logger.error(f"Error in chat disconnect: {str(e)}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            if data['type'] == 'chat_message':
                # Save message to database
                message = await self.save_message(data['message'])
                
                # Broadcast to chat group
                await self.channel_layer.group_send(
                    "chat_room",
                    {
                        "type": "chat_message",
                        "message": data['message'],
                        "sender": message.sender.username,
                        "timestamp": message.timestamp.isoformat()
                    }
                )
        except Exception as e:
            logger.error(f"Error in chat receive: {str(e)}")

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                "type": "chat_message",
                "message": event["message"],
                "sender": event["sender"],
                "timestamp": event["timestamp"]
            }))
        except Exception as e:
            logger.error(f"Error in chat_message: {str(e)}")

    @database_sync_to_async
    def save_message(self, message_text):
        # You'll need to modify this based on your actual user authentication
        from django.contrib.auth import get_user_model
        User = get_user_model()
        default_user = User.objects.first()  # For testing only
        
        message = Message.objects.create(
            sender=default_user,
            receiver=default_user,  # For testing, sending to self
            message=message_text
        )
        return message