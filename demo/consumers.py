from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from appointment.models import Appointment
from datetime import date
from authuser.models import CustomUser
from appointment.AppointmentSerializer import AppointmentSerializer

class IndexPageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Connect WebSocket and add to group."""
        await self.accept()
        await self.channel_layer.group_add('index_page', self.channel_name)

        # Initialize filters (These will be set in receive)
        self.filter_status = None
        self.filter_date = None
        self.filter_phone = None
        self.filter_role = None

    async def receive(self, text_data):
        """Receive filter parameters from frontend."""
        data = json.loads(text_data)

        # Store filter parameters from frontend
        self.filter_status = data.get("status", "pending")
        self.filter_date = data.get("date", date.today().strftime("%Y-%m-%d"))  
        self.filter_phone = data.get("phone", None)
        self.filter_role = data.get("role", "assigned_to")  

        # Validate user
        try:
            self.user = await sync_to_async(CustomUser.objects.get)(phone=self.filter_phone)
        except CustomUser.DoesNotExist:
            await self.send(text_data=json.dumps({"error": "User not found"}))
            return

        # Fetch filtered data asynchronously
        initial_data = await self.get_posts(self.filter_status, self.filter_date, self.user, self.filter_role)

        # Send JSON response
        await self.send(text_data=json.dumps(initial_data))

    async def disconnect(self, close_code):
        """Disconnect WebSocket and remove from group."""
        await self.channel_layer.group_discard('index_page', self.channel_name)

    async def update_index_page(self, event):
        """Send real-time updates to WebSocket clients, but only if relevant."""
        print("Event received in consumer:", event)  # Ensure the event is received
        updated_data = event.get('data', {})
        print("Updated data:", updated_data)

        # Check if the update is relevant for this client
        is_relevant = (
            updated_data.get("status") == self.filter_status and
            updated_data.get("date") == self.filter_date and
            (
                (self.filter_role == "assigned_to" and updated_data.get("assigned_to") == self.filter_phone) or
                (self.filter_role == "created_by" and updated_data.get("created_by") == self.filter_phone)
            )
        )

        if is_relevant:
            await self.send(text_data=json.dumps({"updated_appointment": updated_data}))

    @sync_to_async
    def get_posts(self, status, filter_date, user, role):
        """Fetch appointments based on filters."""
        try:
            filter_date = date.fromisoformat(filter_date)  
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

        # Apply role-based filtering
        if role == "assigned_to":
            posts = Appointment.objects.filter(status=status, date=filter_date, assigned_to=user)
        else:
            posts = Appointment.objects.filter(status=status, date=filter_date, created_by=user)

        return AppointmentSerializer(posts, many=True).data
