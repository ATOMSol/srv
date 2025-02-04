from rest_framework import serializers
from authuser.models import CustomUser  # Ensure you are importing the right model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Correct model name
        exclude = ['password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']

class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.IntegerField(read_only=True)  # Mark username as read-only
    id = serializers.IntegerField(read_only=True)          # Prevent `id` from being updated

    class Meta:
        model = CustomUser  # Correct model name
        exclude = ['password', 'id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set required=False for all fields except excluded ones
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.exclude:
                field.required = False
