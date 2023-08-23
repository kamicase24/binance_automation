"""Permissions"""
import logging
from re import escape
from rest_framework.permissions import BasePermission
from binance_automation.users.models.user import User

log = logging.getLogger(__name__)

class isAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_superuser:
            return True
        return False

class isExternalUser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_external or request.user.is_superuser:
            return True
        return False

