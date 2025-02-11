# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
# import logging

# logger = logging.getLogger(__name__)

# class CallLiveConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         """Connect WebSocket and add to group."""
#         await self.accept()
#         await self.channel_layer.group_add('call_live', self.channel_name)
#         logger.info(f"✅ WebSocket {self.channel_name} connected and added to group.")

#     async def disconnect(self, close_code):
#         """Disconnect WebSocket and remove from group."""
#         await self.channel_layer.group_discard('call_live', self.channel_name)
#         logger.warning(f"❌ WebSocket {self.channel_name} disconnected with code {close_code}")

#     async def call_notify(self, event):
#         """Handle call_notify message type."""
#         data = event['data']
#         logger.info(f"📞 Call Notification Sent: {data}")

#         # Convert UUID objects to strings (Avoid JSON errors)
#         data['sender'] = str(data['sender'])
#         data['receiver'] = str(data['receiver'])

#         await self.send(text_data=json.dumps({
#             'type': 'call_notify',
#             'data': data
#         }))



from channels.generic.websocket import AsyncWebsocketConsumer
import json
import uuid
import logging

logger = logging.getLogger(__name__)

class CallLiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect WebSocket and add user to their personal notification group."""
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]  # Fetch user_id from URL
        self.user_group_name = f"user_{self.user_id}"  # Unique group for each user

        await self.channel_layer.group_add(self.user_group_name, self.channel_name)
        await self.accept()

        logger.info(f"✅ WebSocket {self.channel_name} connected to {self.user_group_name}.")

    async def disconnect(self, close_code):
        """Remove user from personal notification group on disconnect."""
        await self.channel_layer.group_discard(self.user_group_name, self.channel_name)
        logger.warning(f"❌ WebSocket {self.channel_name} disconnected from {self.user_group_name}")

    async def call_notify(self, event):
        """Send call notification only to the intended receiver."""
        data = event["data"]

        # Ensure `receiver` and `sender` are UUID strings
        if isinstance(data.get("receiver"), uuid.UUID):
            data["receiver"] = str(data["receiver"])
        
        if isinstance(data.get("sender"), uuid.UUID):
            data["sender"] = str(data["sender"])

        logger.info(f"📞 Call Notification for Receiver {data['receiver']}: {data}")

        await self.send(text_data=json.dumps({
            "type": "call_notify",
            "data": data
        }))
