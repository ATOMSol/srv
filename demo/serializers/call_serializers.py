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




# class CallNotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CallNotification
#         fields = ['call_id', 'timestamp', 'read', 'sender', 'receiver']

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['sender'] = str(instance.sender)  # Convert UUID to string
#         data['receiver'] = str(instance.receiver)
#         return data

# class CallNotificationSerializer(serializers.ModelSerializer):
#     sender = serializers.StringRelatedField()
#     # receiver = serializers.SerializerMethodField()

#     class Meta:
#         model = CallNotification
#         fields = ['call_id', 'timestamp', 'read', 'sender', 'receiver']

#     def get_sender(self, obj):
#         return str(obj.sender)


class CallNotificationSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    call_id = serializers.UUIDField(format='hex')  # Ensures UUID is serialized as a string

    class Meta:
        model = CallNotification
        fields = ['call_id', 'timestamp', 'read', 'sender', 'receiver']

    def get_sender(self, obj):
        return obj.sender.phone  # Use sender's phone number instead of UUID

    def get_receiver(self, obj):
        return str(obj.receiver)  # Use receiver's phone number