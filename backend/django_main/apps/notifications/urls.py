"""
Notifications app URL configuration
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = "notifications"

router = DefaultRouter()

urlpatterns = router.urls
