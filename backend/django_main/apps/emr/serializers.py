"""
Serializers for EMR app.
"""
from rest_framework import serializers
from apps.emr.models import Patient, Encounter, FormSOAP, FormVitals, MergedDocument
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class PatientSerializer(serializers.ModelSerializer):
    """Patient serializer."""
    
    full_name = serializers.CharField(source='full_name', read_only=True)
    age = serializers.IntegerField(source='get_age', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class EncounterSerializer(serializers.ModelSerializer):
    """Encounter serializer."""
    
    class Meta:
        model = Encounter
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FormSOAPSerializer(serializers.ModelSerializer):
    """SOAP chart serializer."""
    
    class Meta:
        model = FormSOAP
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FormVitalsSerializer(serializers.ModelSerializer):
    """Vital signs serializer."""
    
    class Meta:
        model = FormVitals
        fields = '__all__'
        read_only_fields = ['id', 'bmi', 'bmi_status', 'created_at', 'updated_at']


class MergedDocumentSerializer(serializers.ModelSerializer):
    """Merged document serializer."""
    
    class Meta:
        model = MergedDocument
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
