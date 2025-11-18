from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lectura permitida a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        # Edición solo al dueño
        return obj.owner == request.user

