from rest_framework.permissions import BasePermission

class IsAdminOrStaff(BasePermission):

    message = "You do not have the required permission to perform this action"

    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_staff or request.user.is_uch or request.user.is_core

