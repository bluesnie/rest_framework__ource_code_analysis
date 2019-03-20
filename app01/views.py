import json

from django.shortcuts import render
from django.views import View

from django.http import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.permissions import BasePermission
from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning,NamespaceVersioning
from app01.utils.permission import VipPermission
from app01.models import UserInfo, UserToken


# Create your views here.










###################### 第一部分




# 访问进来第一步执行as_view()里面的view()里面的dispath,当前类没有找父类
class MyAuthentication(object):
    """
    认证源码流程
    1.访问进来第一步执行dispath,当前类没有找父类
    2.封装Request：               initialize_request(request, *args, **kwargs)
    3.                            initial(request, *args, **kwargs)           #    这当中我们设置的raise异常都会在当前函数的下面捕获
    4.                            perform_authentication(request)
    5.                            request.user ————>去封装request的类里面找user()方法
    6.user方法里面:                _authenticate()
    7._authenticate()里面循环认证类的所有对象       调用每个对象的authenticate()方法就是我们自己定义的 MyAuthentication里面的 authenticate()
    8.最后反射到我们定义的View的get,post等等方法执行里面逻辑。

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
    # 因为全局配置了，但当前View认证，所以设置为空
    authentication_classes = []

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

# 认证类移到utils里的auth文件
# token认证，需要登录的view都可以用authentication_classes = [Authentication,]指明
# class Authentication(object):
#
#     def authenticate(self, request):
#         token = request._request.GET.get('token')
#         token_obj = UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed('用户认证失败')
#         # 在rest framework内部会将这两个字段赋值给request，以供后面使用
#         return (token_obj.user, token_obj)
#
#     def authenticate_header(self, val):
#         pass


# 权限类，写在permission.py中
# class MyPermission2(object):
#
#     def has_permission(self, request, view):
#         print(request.user)
#         if request.user.user_type != 3:
#             return False
#         return True
# class MyPermission1(object):
#
#     def has_permission(self, request, view):
#         print(request.user)
#         if request.user.user_type != 1:
#             return False
#         return True

# 版本类(自定义)
class ParamVersion(object):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get('version')
        return version
# 自带的from rest_framework.versioning import QueryParameterVersioning, URLPathVersioning

class OrderView(APIView):
    """订单相关业务（只让svip访问）"""
    # 加个认证类(在settings中设置)
    # authentication_classes = [Authentication,]
    # permission_classes = [SvipPermission,]
    # 版本自定义
    # versioning_class = ParamVersion
    # 版本自带推荐使用(url里配置)
    # versioning_class = URLPathVersioning

    def get(self, request, *args, **kwargs):
        self.dispatch()
        # 前面认证返回的可以这样取
        # request.user
        # request.auth

        # 获取版本
        # print(request.version)
        # 获取处理版本的对象
        # print(request.versioning_scheme)
        # request.versioning_scheme
        # print(request.versioning_scheme.reverse(viewname='order', request=request))

        ret = {'code': 10000,'msg': None, 'data':None}
        try:
            ret['data'] = ORDER_DICT
        except Exception as e:
            pass
        return JsonResponse(ret)


class UserInfoView(APIView):
    """用户中心（普通用户，vip）"""
    # authentication_classes = [Authentication, ]
    # 当前permission_classes存在就不会去取配置文件里的设置
    permission_classes = [VipPermission, ]

    def get(self, request, *args, **kwargs):
        return HttpResponse('用户信息')


# 解析器
from rest_framework.parsers import JSONParser, FormParser


class ParserView(APIView):
    # 全局配置
    # parser_classes = [JSONParser, FormParser]
    """
    JSONParser:表示只能解析content-type:application/json头,(最常用)
    FormParser:表示只能解析content-type:application/x-www-form-urlencoded头
    """

    def post(self, request, *args, **kwargs):
        """
        允许用户发送JSON格式数据
            a.content-type:application/json
            b.{'name':'alex','age':18}
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 获取解析后的结果，用了request.data才去解析
        """
            1.获取用户请求
            2.获取用户请求体
            3.根据用户请求体和parser_classes = [JSONParser,]中支持的请求头进行比较
            4.JSONParser对象处理请求体
            5.request.data来触发的
        """
        print(request.data)

        return  HttpResponse('ParserView')


