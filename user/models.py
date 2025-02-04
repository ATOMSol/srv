from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
        ('gm', 'GM'),
        ('pa', 'PA'),
    )
class User(AbstractUser):
    # Add other custom fields if needed
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='pa'
    )
    gm = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='team_members')

    

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
