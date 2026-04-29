# backend/core/permissions.py
from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow only owner of booking or admin/staff"""
    def has_object_permission(self, request, view, obj):
        # Admin or staff can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Regular user can only access their own bookings
        return obj.user == request.user

class IsBookingPending(permissions.BasePermission):
    """Only allow payment/cancel if booking is pending"""
    def has_object_permission(self, request, view, obj):
        return obj.status == "pending"

class IsNotBookedSeat(permissions.BasePermission):
    """Custom permission for seat selection - prevent double booking"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # For POST (seat selection), we'll check in view
        return True