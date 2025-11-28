"""
ViewSets for Custom app - Brain tumor diagnosis features.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.custom.models import (
    Doctor,
    PatientDoctor,
    Appointment,
    PatientPredictionResult,
    Prescription
)
from apps.custom.serializers import (
    DoctorSerializer,
    PatientDoctorSerializer,
    AppointmentSerializer,
    PatientPredictionResultSerializer,
    PrescriptionSerializer
)
from apps.custom.permissions import (
    IsDoctorOrAdmin,
    CanAccessAppointments,
    CanManageAppointments,
    CanAccessPredictionResults,
    CanAccessPrescriptions
)
import logging

logger = logging.getLogger(__name__)


class DoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Doctor management.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrAdmin]
    filterset_fields = ['specialty', 'department']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialty']
    ordering_fields = ['created_at', 'specialty']


class PatientDoctorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Patient-Doctor relationship management.
    """
    queryset = PatientDoctor.objects.all()
    serializer_class = PatientDoctorSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['patient', 'doctor', 'is_primary']
    ordering_fields = ['assigned_date', 'created_at']


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Appointment management.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, CanAccessAppointments]
    filterset_fields = ['patient', 'doctor', 'status', 'visit_type']
    search_fields = ['patient__full_name', 'reason']
    ordering_fields = ['scheduled_at', 'created_at']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, CanManageAppointments])
    def confirm(self, request, pk=None):
        """Confirm an appointment."""
        appointment = self.get_object()
        appointment.confirm()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, CanManageAppointments])
    def cancel(self, request, pk=None):
        """Cancel an appointment."""
        appointment = self.get_object()
        appointment.cancel()
        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class PatientPredictionResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AI Prediction Results.
    """
    queryset = PatientPredictionResult.objects.all()
    serializer_class = PatientPredictionResultSerializer
    permission_classes = [IsAuthenticated, CanAccessPredictionResults]
    filterset_fields = ['patient', 'encounter', 'prediction_class', 'doctor_feedback']
    ordering_fields = ['created_at', 'confidence_score']


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Prescription management.
    """
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated, CanAccessPrescriptions]
    filterset_fields = ['encounter']
    ordering_fields = ['prescribed_at', 'created_at']
