from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS

User = get_user_model()


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if request.method in SAFE_METHODS:
            return True
        elif user is None:
            return False
        else:
            if user.is_staff:
                return True
            return user == obj.user


class IsPremium(BasePermission):
    def __init__(self, read_only=False):
        self.read_only = read_only

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff:
            return True
        if self.read_only:
            return request.method in SAFE_METHODS
        return user.is_premium


class IsFreelancer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_freelancer
