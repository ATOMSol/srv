from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from authuser.models import CustomUser
from .models import CallNotification,Snacks,Order,ScreenActivity
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from .serializers.call_serializers import CallNotificationSerializer,ContactListSerializer
from .serializers.canteen_serializers import SnacksSerializer,OrderSerializer,GetOrderSerializer
from django.contrib.auth.hashers import check_password
from appointment.models import Appointment
from .serializers.live_appoint_serializers import DisplayAppointmentSerializer
from django.utils.timezone import localtime

class BaseAuthentication(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication,SessionAuthentication]
    permission_classes = [IsAuthenticated]


def index1(request):
    return render(request, 'demo/index.html')

# API View for creating a notification
class CallGenerate(BaseAuthentication):
    def list(self, request):
        unread_calls = CallNotification.objects.filter(receiver=request.user, read=False)
        serializer = CallNotificationSerializer(unread_calls, many=True)
        return Response({
            "RES": serializer.data,
            "count": unread_calls.count(),
            "message": "Fetched successfully." if unread_calls.exists() else "No unread calls."
        })

    

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
            # print(request.GET.get("gm_id"))
            data=CustomUser.objects.filter(gm=request.GET.get("gm_id"))
            serial=ContactListSerializer(data,many=True)
            return Response({'RES':serial.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to log out'}, status=status.HTTP_400_BAD_REQUEST)
        

class AcceptCall(BaseAuthentication):
    def create(self, request):
        if not request.data.get('call_id'):
            return Response({'ERR': 'Call id required'}, status=status.HTTP_400_BAD_REQUEST)

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
        serial=GetOrderSerializer(Order.objects.filter(created_at__date= localtime().date()), many=True)
        return Response({"RES":serial.data})



class CheckUserViewSet(viewsets.ViewSet):
    def create(self, request):
        screen_id = request.data.get("screen_id")
        password = request.data.get("password")

        if not screen_id or not password:
            return Response({"ERR": "Screen ID and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            screen_activity = ScreenActivity.objects.get(screen_id=screen_id)

            if check_password(password, screen_activity.password):
                screen_activity.is_active=True
                screen_activity.save()
                display_user = screen_activity.live_user
                return Response({
                    "RES": [
                        {
                            "screen_id":screen_activity.screen_id,
                            "live_fetch_id": display_user.unique_id,
                            "phone": display_user.email,  # Assuming email is used as phone
                            "name": display_user.phone
                        }
                    ]
                }, status=status.HTTP_200_OK)
            else:
                return Response({"ERR": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

        except ScreenActivity.DoesNotExist:
            return Response({"ERR": "Screen ID not found"}, status=status.HTTP_404_NOT_FOUND)


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


class ActiveDisplay(BaseAuthentication):
    def create(self, request):
        try:
            ob = ScreenActivity.objects.get(screen_id=request.data.get("screen_id"))  # ✅ screen_id
            ob.is_active = True
            ob.live_user = request.user
            ob.updated_at = request.user
            ob.save()
            return Response({"RES": True, "display_id": ob.id})  # ✅ Return RES and display_id
        except Exception as e:
            print(e)
            return Response({"ERR": False})


class DeActiveDisplay(BaseAuthentication):
    def create(self, request):
        # print(request.data)
        try:
            ob = ScreenActivity.objects.get(id=request.data.get("id"))  # ✅ id
            ob.is_active = False
            ob.live_user = None
            ob.updated_at = request.user
            ob.save()
            return Response({"RES": True})  # ✅ Return RES
        except Exception as e:
            print(e)
            return Response({"ERR": False})
