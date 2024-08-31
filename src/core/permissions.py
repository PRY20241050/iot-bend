from rest_framework.permissions import BasePermission


class IsBrickyard(BasePermission):
    """
    Custom permission to only allow brickyard to view the object.
    """

    def has_permission(self, request, view):
        return request.user.brickyard is not None


class IsInstitution(BasePermission):
    """
    Custom permission to only allow institution to view the object.
    """

    def has_permission(self, request, view):
        return request.user.institution is not None


class IsOwner(BasePermission):
    """
    Custom permission to only allow owner of an object to view or edit it.
    You need to add is_owner method to the model to use this permission.

    Example:
        In your model:
        def is_owner(self, user):
            return self.user == user
    """

    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)
