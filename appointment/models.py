from django.db import models
from authuser.models import CustomUser
import uuid
# from django.core.exceptions import ValidationError


STATUS_CHOICES = (
        ('pending','pending'),
        ('in_progress', 'In Progress'),
        ('completed','Completed'),
        ('next','Next'),
)
class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visitor_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    description = models.TextField(blank=True)
    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default="pending",
        )  # Status field (Pending, In Progress, Completed)
    
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_appointments",limit_choices_to={'roles__name': 'gm'}
    ) 
    company_name = models.CharField(max_length=100,default="NA")
    company_address = models.CharField(max_length=100,default="NA")
    purpose_of_visit = models.CharField(max_length=100,default="Na")
    visitor_img = models.ImageField(upload_to='visitor_img/' ,blank=True)  # 'product_images/' is the folder where the image will be saved

    # Add creation and update tracking fields
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Automatically updated on save
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_appointments",limit_choices_to={'roles__name': 'pa'})  # User who created the appointment
    updated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_appointments")  # User who last updated the appointment


    def __str__(self):
        return f"{self.visitor_name} - {self.date}"
    
    
class AdditionalVisitor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    # email = models.EmailField()
    participants = models.ForeignKey(Appointment,on_delete=models.CASCADE, related_name="additional_visitor",default=None)  # Multiple participants
    img = models.ImageField(upload_to='additional_visitor_image/', blank=True)  # 'product_images/' is the folder where the image will be saved

    def __str__(self):
        return self.name