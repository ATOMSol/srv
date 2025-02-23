from rest_framework import serializers
from .models import Appointment, AdditionalVisitor

class AdditionalVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalVisitor
        fields = ['name', 'img']

class AppointmentSerializer(serializers.ModelSerializer):
    additional_visitors = AdditionalVisitorSerializer(many=True, required=False)  # Nested serializer

    class Meta:
        model = Appointment
        fields = [
            'id', 'visitor_name', 'email', 'phone', 'date', 'description',
            'status', 'assigned_to', 'company_name', 'company_address',
            'purpose_of_visit', 'visitor_img', 'created_by', 'updated_by',
            'additional_visitors'
        ]

    def create(self, validated_data):
        additional_visitors_data = validated_data.pop('additional_visitors', [])
        appointment = Appointment.objects.create(**validated_data)

        # Save Additional Visitors
        for visitor_data in additional_visitors_data:
            AdditionalVisitor.objects.create(participants=appointment, **visitor_data)

        return appointment
