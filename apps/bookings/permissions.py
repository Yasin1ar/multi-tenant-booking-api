from rest_framework import permissions
from apps.users.models import User


class IsOrganizationAdmin(permissions.BasePermission):
    """
    Permission check to ensure the user is an ADMIN.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsBookingOwner(permissions.BasePermission):
    """
    Object-level permission allowing booking owners or ADMIN users to access a booking.
    """

    def has_object_permission(self, request, view, obj):
        if not (request.user and request.user.is_authenticated):
            return False

        # 1. Allow if the user owns the booking
        if obj.user == request.user:
            return True

        # 2. Allow if the user is an ADMIN
        return request.user.role == User.Role.ADMIN
