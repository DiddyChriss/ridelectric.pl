from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.assigned_to == request.user:
            return True
        else:
            return False