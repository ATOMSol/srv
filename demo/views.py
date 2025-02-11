from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import CustomUser
from .models import CallNotification,Snacks,Order,ScreenActivity
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from .serializers.call_serializers import CallNotificationSerializer,ContactListSerializer
from .serializers.canteen_serializers import SnacksSerializer,OrderSerializer,GetOrderSerializer

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]


def index1(request):
    return render(request, 'demo/index.html')

# API View for creating a notification
class CallGenerate(BaseAuthentication):
    def create(self,request):
        receiver_id = request.data.get('receiver')
        
        if not receiver_id:
            return Response({'ERR': 'Receiver and message fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            receiver = CustomUser.objects.get(unique_id=receiver_id)
        except CustomUser.DoesNotExist:
            return Response({'ERR': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
        
        notification = CallNotification.objects.create(sender=request.user, receiver=receiver)
        serial = CallNotificationSerializer(notification)
        
        return Response({"RES":True})
    




class ContactList(BaseAuthentication):
    def list(self, request):
        try:
            print(6666)
            data=CustomUser.objects.filter(gm=request.user)
            serial=ContactListSerializer(data,many=True)
            print(serial.data)
            return Response({'RES':serial.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to log out'}, status=status.HTTP_400_BAD_REQUEST)
        

class AcceptCall(BaseAuthentication):
    def create(self, request):
        print(request.data)
        if not request.data.get('call_id'):
            return Response({'ERR': 'Call id required'}, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

        try:
            call_notification = CallNotification.objects.get(call_id=request.data.get('call_id'))
            call_notification.read = True
            call_notification.save()
            return Response({'success': 'Call marked as read'}, status=status.HTTP_200_OK)
        except CallNotification.DoesNotExist:
            return Response({'ERR': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)


# Snacks ViewSet
class SnacksViewSet(viewsets.ReadOnlyModelViewSet):  # Only GET methods allowed
    queryset = Snacks.objects.all()
    serializer_class = SnacksSerializer


class OrderCreateAPIView(BaseAuthentication):
    def create(self, request):
        # Extract `order_data` and rename it to `items`
        data = request.data.copy()
        if "order_data" in data:
            data["items"] = data.pop("order_data")

        # Ensure 'items' exists
        if "items" not in data:  # Fix: It should check for "items" instead of "order_data"
            return Response({"error": "Missing 'items' field"}, status=status.HTTP_400_BAD_REQUEST)

        # Add `created_by` field automatically
        data["created_by"] = request.user.unique_id

        serializer = OrderSerializer(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Order created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OrderHistoryAPIView(viewsets.ViewSet):
    def list(self, request):
        serial=GetOrderSerializer(Order.objects.all(), many=True)
        return Response({"RES":serial.data})



class CheckUserViewSet(viewsets.ViewSet):
    def list(self, request):
        phone = request.GET.get("phone")  # Get phone from query params
        if not phone:
            return Response({"ERR": "Phone number is required"}, status=400)

        try:
            user = CustomUser.objects.get(phone=phone)
            screen_data = ScreenActivity.objects.filter(screen_id=user).values()  # Fetch all related screens

            return Response({
                "RES": list(screen_data),  # Convert queryset to list
                "user": {
                    "phone": user.phone,
                    "name": user.first_name
                }
            })
        except CustomUser.DoesNotExist:
            return Response({"ERR": "User not found"}, status=404)



from rest_framework.decorators import action

class UpdateOrderStatus(viewsets.ViewSet):
    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        try:
            order = Order.objects.get(id=pk)
            order.status = True
            order.save()
            return Response({"success": True, "message": "Order status updated!"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"success": False, "error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
