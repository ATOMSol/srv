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
from django.conf import settings
from django.conf.urls.static import static

# from authuser.views import index
from demo.views import index1

urlpatterns = [
    path('admin/', admin.site.urls),
    path('realtime',index1, name='index1'),
    # path('',index, name='index'),
    path('api/', include('authuser.urls')),
    path('api/', include('appointment.urls')),
    # path('realtime', include('demo.urls')),
    path('api/', include('demo.urls')),
    path('', include('main_server.urls',namespace="main_server")),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)