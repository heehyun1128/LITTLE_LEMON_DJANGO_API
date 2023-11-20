from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff #request.user.is_staff to distinguish regular users from staff/admin users

class isManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='manager').exists()

class IsDeliveryCrewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='delivery_crew').exists()

class IsCustomerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name='customer').exists()