"""
Custom permissions for NeuroNova.
RBAC (Role-Based Access Control) implementation.
"""
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView
from config.constants import UserRole
from typing import Any
import logging

logger = logging.getLogger(__name__)


class IsAdmin(permissions.BasePermission):
    """
    Permission: Only admins can access.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'profile'):
            is_admin = request.user.profile.role == UserRole.ADMIN
            if not is_admin:
                logger.warning(
                    f"Admin access denied for user: {request.user.username}"
                )
            return is_admin

        return request.user.is_staff or request.user.is_superuser


class IsDoctor(permissions.BasePermission):
    """
    Permission: Only doctors can access.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'profile'):
            return request.user.profile.role == UserRole.DOCTOR

        return False


class IsNurse(permissions.BasePermission):
    """
    Permission: Only nurses can access.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'profile'):
            return request.user.profile.role == UserRole.NURSE

        return False


class IsPatient(permissions.BasePermission):
    """
    Permission: Only patients can access.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'profile'):
            return request.user.profile.role == UserRole.PATIENT

        return False


class IsDoctorOrNurse(permissions.BasePermission):
    """
    Permission: Doctors or nurses can access.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        if hasattr(request.user, 'profile'):
            role = request.user.profile.role
            return role in [UserRole.DOCTOR, UserRole.NURSE]

        return False


class CanModifyMedicalData(permissions.BasePermission):
    """
    Permission: Check if user can modify medical data.
    Important: Medical data cannot be deleted, only soft-deleted (updated).
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False

        # DELETE is not allowed for medical data integrity
        if request.method == 'DELETE':
            logger.warning(
                f"DELETE attempt on medical data by user: {request.user.username}"
            )
            return False

        # Doctors can Create, Read, Update
        if hasattr(request.user, 'profile'):
            role = request.user.profile.role
            if role == UserRole.DOCTOR:
                return True
            elif role == UserRole.NURSE:
                # Nurses can only Read and Update Vitals
                return request.method in ['GET', 'PATCH', 'PUT']

        return False
