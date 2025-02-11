from rest_framework.routers import SimpleRouter
from demo.views import CallGenerate, AcceptCall, ContactList, SnacksViewSet, OrderHistoryAPIView,OrderCreateAPIView,CheckUserViewSet,UpdateOrderStatus

api_router = SimpleRouter()
api_router.register(r'call', CallGenerate, basename='call')
api_router.register(r'contact_list', ContactList, basename='contact_list')
api_router.register(r'accept_call', AcceptCall, basename='accept_call')
api_router.register(r'snacks', SnacksViewSet, basename='snacks')
api_router.register(r'order', OrderCreateAPIView, basename='order')
api_router.register(r'order_history', OrderHistoryAPIView, basename='order_history')
api_router.register(r'check-user',CheckUserViewSet, basename='check_user')
api_router.register(r"update_order_status", UpdateOrderStatus, basename="update_order_status")

urlpatterns = api_router.urls
