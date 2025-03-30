from rest_framework.serializers import ModelSerializer
from authuser.models import CustomUser
from demo.models import CallNotification
from rest_framework import serializers
from django.contrib.auth.models import Group

class ContactListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['unique_id', 'first_name','last_name','role']
    # def get_role(self, obj):
    #     role_id = obj.roles.first().id
    #     role = Role.objects.get(id=role_id)
    #     return role.name


    def get_role(self, obj):
        """
        Get the first group name that the user belongs to.
        """
        group = obj.groups.first()  # Fetch the first group assigned to the user
        return group.name.lower() if group else None  # Return group name 

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
    sender_name = serializers.SerializerMethodField()
    sender_role = serializers.SerializerMethodField()  # ✅ Add group name

    call_id = serializers.UUIDField(format='hex')  # Ensures UUID is serialized as a string

    class Meta:
        model = CallNotification
        fields = ['call_id','sender_name','sender_role', 'read', 'sender', 'receiver']

    def get_sender(self, obj):
        return obj.sender.phone  # Use sender's phone number instead of UUID

    def get_receiver(self, obj):
        return str(obj.receiver)  # Use receiver's phone number
    
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()  # First name + Last name

    def get_sender_role(self, obj):
        group = obj.sender.groups.first()  # ✅ Sirf pehla group fetch karega
        return group.name if group else None
