"""
Serializers for Notifications app.
"""
from rest_framework import serializers
from apps.notifications.models import NotificationLog
import logging

logger = logging.getLogger(__name__)


class NotificationLogSerializer(serializers.ModelSerializer):
    """Notification log serializer."""
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = NotificationLog
        fields = '__all__'
        read_only_fields = ['id', 'sent_at', 'created_at', 'updated_at']
