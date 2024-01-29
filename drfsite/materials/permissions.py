from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator')


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
