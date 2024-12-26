from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermission(BasePermission):
    """
    Custom permission to allow only project owners or admins to edit or delete a project.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff

class CommentPermission(BasePermission):
    """
    Custom permission to allow only commenter, project owners or admins to edit or delete a project.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method == "GET":
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow admin to perform any request
        if request.user.is_staff:
            return True
        # Allow commenter to perform any request
        if request.user == obj.user:
            return True
        
        # Allow project owner to perform any request
        if request.user == obj.task.project.owner:
            return True
        return False
    
class TaskPermission(BasePermission):
    """
    Custom permission to allow only project owners or admins to edit or delete a project.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in SAFE_METHODS:
            return True
        return obj.project.owner == request.user or request.user.is_staff
