from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chat'),
    path('appointments/', views.ws_appointments, name='ws_appointments'),
]