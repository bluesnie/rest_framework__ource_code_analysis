# _*_ encoding:utf-8 _*_
from rest_framework import exceptions
from app01.models import UserToken
from rest_framework.authentication import BaseAuthentication


# token认证，需要登录的view都可以用authentication_classes = [Authentication,]指明
# 自定义认证的类都需要继承BaseAuthentication
class Authentication(BaseAuthentication):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest framework内部会将这两个字段赋值给request，以供后面使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, val):
        pass