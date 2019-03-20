# _*_ encoding:utf-8 _*_
from rest_framework.permissions import BasePermission

class SvipPermission(BasePermission):
    message = "必须是SVIP才能访问"

    def has_permission(self, request, view):
        # print(request.user)
        if request.user.user_type != 3:
            return False
        return True


class VipPermission(BasePermission):

    def has_permission(self, request, view):
        # print(request.user)
        if request.user.user_type != 1:
            return False
        return True
