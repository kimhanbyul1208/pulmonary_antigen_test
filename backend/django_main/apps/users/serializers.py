"""
Serializers for Users app.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    """User serializer with profile."""
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'profile']
        read_only_fields = ['id', 'date_joined']
