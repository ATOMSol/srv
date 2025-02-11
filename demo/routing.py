# demo/routing.py
from django.urls import re_path

from .consumers import appointment_consumers,call_consumer,canteen_consumer

websocket_urlpatterns = [
    re_path(r'^ws/appointment/$', appointment_consumers.IndexPageConsumer.as_asgi()),
    # re_path(r'^ws/call/$', call_consumer.CallLiveConsumer.as_asgi()),
    re_path(r"^ws/call/(?P<user_id>[0-9a-fA-F-]+)/$",call_consumer.CallLiveConsumer.as_asgi()),

    re_path(r'^ws/snacks/$', canteen_consumer.OrderLiveConsumer.as_asgi()),

]

