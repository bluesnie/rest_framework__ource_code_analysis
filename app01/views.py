import json

from django.shortcuts import render
from django.views import View

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions

from app01.models import UserInfo, UserToken
# Create your views here.










###################### 第一部分









# 访问进来第一步执行dispath,当前类没有找父类
class MyAuthentication(object):
    """
    认证流程
    1.封装Request：                initialize_request(request, *args, **kwargs)
    2. 认证:                       initial(request, *args, **kwargs)
    3. 实现认证:                    perform_authentication(request)
    4.获取认证对象进行一步步的认证:   _authenticate()
    """
    def authenticate(self, request):
        token = request._request.GET.get('token')
        # 获取用户名和密码，去数据库校验
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 放回元组（校验后的数据）
        return ("nzb", None)

    def authenticate_header(self, val):
        pass

# APIView继承自View
# class OrderView(APIView):
#     authentication_classes = [MyAuthentication,]
#
#     def get(self, request, *args, **kwargs):
#         self.dispatch()
#         # 此时的request不在是原生的request
#         print(request)
#         print(request.user)
#         ret = {
#             'code': 10000,
#             'msg': 'xxx'
#         }
#         return HttpResponse(json.dumps(ret), status=200)
#
#     def post(self, request, *args, **kwargs):
#         return HttpResponse('创建order')
#
#     def put(self, request, *args, **kwargs):
#         return HttpResponse('更新order')
#
#     def delete(self, request, *args, **kwargs):
#         return HttpResponse('删除order')







#################################### 第二部分
#####认证原理









# 生产token函数
def md5(user):
    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

# 实验数据
ORDER_DICT = {
    1:{
        'name':'狗',
        'age':12,
        'gender':'男'
    },
    2:{
        'name':'猫',
        'age':15,
        'gender':'女'
    }
}

# 用户认证
class AuthView(APIView):
    """用户认证"""
    def post(self, request, *args, **kwargs):
        ret = {'code':1000, 'msg':None}
        try:
            user = request._request.POST.get('username', '')
            pwd = request._request.POST.get('password', '')
            obj = UserInfo.objects.filter(username=user, password=pwd).first()
            if not obj:
                ret['code'] = '1001'
                ret['msg'] = '用户名或密码错误'
            # 为登录用户创建token
            token = md5(user)
            # 存在就更新，不存在就创建
            UserToken.objects.update_or_create(user=obj, defaults={'token':token})

        except Exception as e:
            ret['code'] = '1002'
            ret['msg'] = '请求异常'
        return JsonResponse(ret)

# token认证，需要登录的view都可以用authentication_classes = [Authentication,]指明
class Authentication(object):

    def authenticate(self, request):
        token = request._request.GET.get('token')
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed('用户认证失败')
        # 在rest framework内部会将这两个字段赋值给request，以供后面使用
        return (token_obj.user, token_obj)

    def authenticate_header(self, val):
        pass


class OrderView(APIView):
    """订单相关业务"""
    # 加个认证类
    authentication_classes = [Authentication,]

    def get(self, request, *args, **kwargs):
        # 前面认证返回的可以这样取
        # request.user
        # request.auth

        ret = {'code': 10000,'msg': None, 'data':None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """用户中心"""
    authentication_classes = [Authentication, ]

    def get(self, request, *args, **kwargs):
        return HttpResponse('用户信息')


