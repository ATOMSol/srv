# src/urls.py
from django.contrib import admin
from django.urls import include, path

from main_server.views import index,auth,dashboard
from demo.views import index1

urlpatterns = [
    path('',index, name='index'),
    path('auth',auth, name='auth'),
    path('dashboard',dashboard, name='dashboard'),
]