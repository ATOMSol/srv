from rest_framework import serializers
from .models import Appointment, AdditionalVisitor
from urllib.parse import urljoin
from django.conf import settings


class AdditionalVisitorSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()  # ✅ Convert to full URL
    # img = serializers.ImageField(required=False, allow_null=True)  # ✅ Fix: Allows None
    class Meta:
        model = AdditionalVisitor
        exclude = ['id','participants']

    def get_img(self, obj):
        if obj.img:
            return urljoin(settings.DOMAIN_NAME, obj.img.url)
        return None



class AppointmentSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()  # ✅ Custom field for name
    visitor_img = serializers.SerializerMethodField()  # ✅ Convert to full URL
    additional_visitors = AdditionalVisitorSerializer(many=True, read_only=True)
    # visitor_img = serializers.ImageField(required=False, allow_null=True)  # ✅ Fix: Allows file upload

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_visitor_img(self, obj):
        """Convert visitor_img to full URL"""
        if obj.visitor_img:
            return urljoin(settings.DOMAIN_NAME, obj.visitor_img.url)
        return None
    
    def get_assigned_to(self, obj):
        """Return assigned user's full name or username"""
        if obj.assigned_to:
            full_name = f"{obj.assigned_to.first_name} {obj.assigned_to.last_name}".strip()
            return full_name if full_name else obj.assigned_to.phone  # Fallback to username
        return None