from rest_framework import serializers
from appointment.models import Appointment
from urllib.parse import urljoin
from django.conf import settings



# class DisplayAppointmentSerializer(serializers.ModelSerializer):
#     visitor_img = serializers.SerializerMethodField()  # ✅ To get full image URL

#     # ✅ Explicitly convert UUID fields to CharField (string in JSON)
#     id = serializers.CharField()  # Appointment ID as string
#     assigned_to = serializers.CharField(source='assigned_to_id', allow_null=True)  # FK ID as string, nullable
#     created_by = serializers.CharField(source='created_by_id', allow_null=True)  # FK ID as string, nullable

#     class Meta:
#         model = Appointment
#         fields = '__all__'

#     def get_visitor_img(self, obj):
#         """Convert visitor_img to full URL"""
#         if obj.visitor_img:
#             return urljoin(settings.DOMAIN_NAME, obj.visitor_img.url)
#         return None

    

class DisplayAppointmentSerializer(serializers.ModelSerializer):
    id = serializers.CharField()  # Appointment ID as string
    assigned_to = serializers.CharField(source='assigned_to_id', allow_null=True)  # FK ID as string, nullable
    created_by = serializers.CharField(source='created_by_id', allow_null=True)  # FK ID as string, nullable
    gm_name = serializers.SerializerMethodField()  # ✅ To get assigned GM name
    company_display_name = serializers.SerializerMethodField()  # ✅ Custom field for company or visitor name

    class Meta:
        model = Appointment
        fields = [
            'id', 
            'assigned_to', 
            'gm_name', 
            'created_by', 
            'status',
            'company_display_name'  # ✅ Make sure this field is included here
        ]

    def get_gm_name(self, obj):
        return obj.assigned_to.first_name if obj.assigned_to else None

    def get_company_display_name(self, obj):
        """
        Return company name if valid, else visitor name.
        """
        if obj.company_name and obj.company_name != "NA":
            return obj.company_name
        return obj.visitor_name
