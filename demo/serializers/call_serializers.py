from rest_framework.serializers import ModelSerializer
from authuser.models import CustomUser,Role
from demo.models import CallNotification
from rest_framework import serializers

class ContactListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['unique_id', 'first_name','last_name','role']
    def get_role(self, obj):
        role_id = obj.roles.first().id
        role = Role.objects.get(id=role_id)
        return role.name

# class CallNotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CallNotification
#         fields = '__all__'




class CallNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    # receiver = serializers.SerializerMethodField()

    class Meta:
        model = CallNotification
        fields = ['call_id', 'timestamp', 'read', 'sender', 'receiver']

    def get_sender(self, obj):
        return obj.sender