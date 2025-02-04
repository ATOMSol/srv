from rest_framework import serializers
from appointment.models import Appointment, AdditionalVisitor
from django.urls import reverse
from django.conf import settings

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalVisitor
        fields = ['name', 'img']


    def to_representation(self, instance):
            # Get the representation of the instance
            representation = super().to_representation(instance)
            
            # Get the image URL and append the domain name
            if instance.img:
                image_url = instance.img.url
                # Use the domain name of the site to build the absolute URL
                full_image_url = f"{settings.DOMAIN_NAME}{image_url}"  # Make sure DOMAIN_NAME is set in settings.py
                representation['img'] = full_image_url
            
            return representation

class AppointmentSerializer(serializers.ModelSerializer):
    additional_visitor = ParticipantSerializer(many=True)  # To handle multiple participants

    class Meta:
        model = Appointment
        fields = ['id','visitor_name', 'email', 'phone', 'date', 'description', 'status', 'assigned_to','company_name','company_address','purpose_of_visit' ,'additional_visitor']
        extra_kwargs = {
                    'created_by': {'read_only': False, 'write_only': True},
                    'assigned_to': {'read_only': False, 'write_only': True}
        }
    def create(self, validated_data):
        # Extract participants from validated data
        participants_data = validated_data.pop('additional_visitor', [])
        
        # Create the appointment
        # appointment = Appointment.objects.create(**validated_data)
        appointment = Appointment.objects.create(created_by=self.context['request'].user, assigned_to=self.context['request'].user.gm, **validated_data)
   
        # Create participants
        for participant_data in participants_data:
            AdditionalVisitor.objects.create(participants=appointment, **participant_data)
        
        return appointment


    def to_representation(self, instance):
            # Get the representation of the instance
            representation = super().to_representation(instance)
            
            # Get the image URL and append the domain name
            if instance.visitor_img:
                image_url = instance.visitor_img.url
                # Use the domain name of the site to build the absolute URL
                full_image_url = f"{settings.DOMAIN_NAME}{image_url}"  # Make sure DOMAIN_NAME is set in settings.py
                representation['visitor_img'] = full_image_url
            
            return representation