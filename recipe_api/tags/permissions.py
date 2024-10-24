from rest_framework.permissions import BasePermission


class TagPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            return request.user.is_authenticated
        if request.method in ("PUT", "PATCH", "DELETE"):
            return request.user.is_authenticated and obj.user == request.user
        return False
