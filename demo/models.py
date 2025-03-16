from django.db import models
from authuser.models import CustomUser
import uuid
from django.contrib.auth.hashers import make_password


class CallNotification(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_notifications')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    call_id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}'
    


class Snacks(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SnacksItem(models.Model):
    category = models.ForeignKey(Snacks, on_delete=models.CASCADE, related_name="SnacksItem")
    name = models.CharField(max_length=200)
    image = models.FileField(upload_to='Snacks/' ,blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Order(models.Model):
    items = models.JSONField()  # Store ordered items in JSON format
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_created_by",limit_choices_to={'roles': 1})  # CustomUser who created the appointment
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_updated_by")  # CustomUser who last updated the appointment
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    def __str__(self):
        return f"Order {self.id} - {self.created_at}"




class ScreenActivity(models.Model):
    screen_id = models.CharField(max_length=100,null=True,blank=True)
    live_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    password = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if password is not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)