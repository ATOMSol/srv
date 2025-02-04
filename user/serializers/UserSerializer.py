from rest_framework.serializers import ModelSerializer
from user.models import User  # Use Django's default User model
# from rest_framework import serializers
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions']
        # fields = '__all__'




class UpdateProfileSerializer(serializers.ModelSerializer):
    username = serializers.IntegerField(read_only=True)  # Mark id as read-only
    id = serializers.IntegerField(read_only=True)          # Prevent `id` from being updated

    class Meta:
        model = User
        exclude = ['password', 'id', 'last_login','is_superuser','is_staff','is_active','date_joined','groups','user_permissions']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set required=False for all fields except excluded ones
        for field_name, field in self.fields.items():
            if field_name not in self.Meta.exclude:
                field.required = False