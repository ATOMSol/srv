from rest_framework.serializers import ModelSerializer
from demo.models import Snacks, SnacksItem,Order
from rest_framework import serializers
from authuser.models import CustomUser

class SnacksItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnacksItem
        fields = ["id", "name", "image"]

class SnacksSerializer(serializers.ModelSerializer):
    items = SnacksItemSerializer(many=True, source="SnacksItem")  # Using related_name

    class Meta:
        model = Snacks
        fields = ["id", "name", "items"]




class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "items", "status", "created_by", "updated_by", "created_at", "updated_at"]
        read_only_fields = ["id", "created_by", "updated_by", "created_at", "updated_at"]

    def create(self, validated_data):
        # Set the created_by field automatically from request context
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by"] = request.user

        return super().create(validated_data)




class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details in the order response."""
    class Meta:
        model = CustomUser
        fields = ["phone","first_name","last_name"]  # Add other fields if needed

from django.utils.timezone import localtime

class GetOrderSerializer(serializers.ModelSerializer):
    """Serializer for Order, including user details."""
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

        def to_representation(self, instance):
                data = super().to_representation(instance)

                # ✅ Timezone conversion to Asia/Kolkata
                indian_tz = pytz.timezone("Asia/Kolkata")
                if instance.created_at:
                    data["created_at"] = localtime(instance.created_at).strftime("%Y-%m-%d %H:%M:%S")
                if instance.updated_at:
                    data["updated_at"] = localtime(instance.updated_at).strftime("%Y-%m-%d %H:%M:%S")

                return data