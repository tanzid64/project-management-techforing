from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdminOnly(BasePermission):
    """
    Custom permission to allow only project owners or admins to edit or delete a project.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff
