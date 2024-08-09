from rest_framework.permissions import BasePermission


class IsBrickyard(BasePermission):
    def has_permission(self, request, view):
        return request.user.brickyard is not None


class IsInstitution(BasePermission):
    def has_permission(self, request, view):
        return request.user.institution is not None


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_owner(request.user)
