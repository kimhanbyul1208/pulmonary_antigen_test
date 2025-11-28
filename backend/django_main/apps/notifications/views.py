"""
ViewSets for Notifications app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.notifications.models import NotificationLog
from apps.notifications.serializers import NotificationLogSerializer
import logging

logger = logging.getLogger(__name__)


class NotificationLogViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification log management."""
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['recipient', 'notification_type', 'is_read']
    ordering_fields = ['sent_at', 'created_at']
