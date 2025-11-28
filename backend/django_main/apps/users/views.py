"""
ViewSets for Users app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from apps.users.serializers import UserSerializer, UserProfileSerializer
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for User (read-only)."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['username', 'email', 'first_name', 'last_name']


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile management."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['role']
    search_fields = ['user__username', 'phone_number']
