from rest_framework import permissions


class MarketOwnEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class BookOwnEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.market.owner


class UserEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id


class BranchContactEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.market.owner


