# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.urls import include, path, re_path

# from webshocket.views import index, ws_appointments

# urlpatterns = [
#     path('admin/', admin.site.urls),
# #    path("", index),
#     path('api/', include('appointment.urls')),
#     path('api/', include('user.urls')),
#     path('websocket/', include('webshocket.urls')),
#     #path('api/appointments/', ws_appointments, name='ws_appointments'),


# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# src/urls.py
from django.contrib import admin
from django.urls import include, path

from authuser.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('api/', include('authuser.urls')),
    path('api/', include('appointment.urls')),
    path('realtime', include('demo.urls')),
]