from rest_framework import serializers
from authuser.models import CustomUser  # Ensure you are importing the right model
# from authuser.models import Role
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['unique_id', 'first_name', 'last_name', 'email', 'pass_key', 'phone', 'gm', 'role']

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

# class UpdateProfileSerializer(serializers.ModelSerializer):
#     username = serializers.IntegerField(read_only=True)  # Mark username as read-only
#     id = serializers.IntegerField(read_only=True)          # Prevent `id` from being updated

#     class Meta:
#         model = CustomUser  # Correct model name
#         exclude = ['password', 'id', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # Set required=False for all fields except excluded ones
#         for field_name, field in self.fields.items():
#             if field_name not in self.Meta.exclude:
#                 field.required = False
