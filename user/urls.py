
from django.urls import path,include

from rest_framework import routers
from .views import LoginAPI,LogoutView

router = routers.DefaultRouter()
router.register(r'login', LoginAPI, basename='login')
router.register(r'logout', LogoutView, basename='logout')

urlpatterns = router.urls
