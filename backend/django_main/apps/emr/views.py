"""
ViewSets for EMR app.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.emr.models import Patient, Encounter, FormSOAP, FormVitals, MergedDocument
from apps.emr.serializers import (
    PatientSerializer,
    EncounterSerializer,
    FormSOAPSerializer,
    FormVitalsSerializer,
    MergedDocumentSerializer
)
from apps.core.permissions import IsDoctorOrNurse
import logging

logger = logging.getLogger(__name__)


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient management."""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrNurse]
    filterset_fields = ['gender', 'blood_type']
    search_fields = ['full_name', 'patient_id', 'phone_number']
    ordering_fields = ['created_at', 'date_of_birth']


class EncounterViewSet(viewsets.ModelViewSet):
    """ViewSet for Encounter management."""
    queryset = Encounter.objects.all()
    serializer_class = EncounterSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrNurse]
    filterset_fields = ['patient', 'encounter_type']
    ordering_fields = ['encounter_date', 'created_at']


class FormSOAPViewSet(viewsets.ModelViewSet):
    """ViewSet for SOAP chart management."""
    queryset = FormSOAP.objects.all()
    serializer_class = FormSOAPSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrNurse]
    filterset_fields = ['encounter']
    ordering_fields = ['created_at']


class FormVitalsViewSet(viewsets.ModelViewSet):
    """ViewSet for Vital signs management."""
    queryset = FormVitals.objects.all()
    serializer_class = FormVitalsSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrNurse]
    filterset_fields = ['encounter']
    ordering_fields = ['created_at']


class MergedDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for Merged document management."""
    queryset = MergedDocument.objects.all()
    serializer_class = MergedDocumentSerializer
    permission_classes = [IsAuthenticated, IsDoctorOrNurse]
    filterset_fields = ['encounter', 'document_type']
    ordering_fields = ['created_at']
