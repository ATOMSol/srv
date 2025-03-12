from rest_framework import serializers
from appointment.models import Appointment
from urllib.parse import urljoin
from django.conf import settings

class AppointmentSerializer(serializers.ModelSerializer):
    visitor_img = serializers.SerializerMethodField()  # ✅ Convert to full URL
    class Meta:
        model = Appointment
        fields = '__all__'

    def get_visitor_img(self, obj):
        """Convert visitor_img to full URL"""
        if obj.visitor_img:
            return urljoin(settings.DOMAIN_NAME, obj.visitor_img.url)
        return None