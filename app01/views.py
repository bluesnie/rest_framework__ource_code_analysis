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
from app01.models import UserInfo, UserToken, Role, UserGroup


# Create your views here.

# 认证
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


#####认证原理
def md5(user):
    """
    生成token
    :param user:
    :return:
    """
    import hashlib
    import time

    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


# 测试数据
ORDER_DICT = {
    1: {
        'name': '狗',
        'age': 12,
        'gender': '男',
    },
    2: {
        'name': '猫',
        'age': 15,
        'gender': '女',
    },
}


# 用户认证
class AuthView(APIView):
    """用户认证"""
    # 因为全局配置了，但当前View认证，所以设置为空
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': None}
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
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})

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


# 用户序列化
from rest_framework import serializers

# 方式一：继承serializers.Serializer
# class UserInfoSerializer(serializers.Serializer):
#
#     username = serializers.CharField()
#     password = serializers.CharField()

#     # source 属性是对应model的字段，所以这里可以自定义名称,当一个表有choice,ForeignKey时都可以用source指定
#     # xxx = serializers.CharField(source="get_user_type_display")
#     user_type = serializers.CharField(source="get_user_type_display") # row.get_user_type_display
#     gorup = serializers.CharField(source="group.name")

#     # ManyToMany则不适合
#     # roles = serializers.CharField(source="roles.all")
#
#     # 自定义显示，上面的choice和ForeignKey也可以这样。
#     roles = serializers.SerializerMethodField() # 自定义显示
#
#     def get_roles(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id':item.id, 'name':item.name})
#         return ret

# 方式二：继承serializers.ModelSerializer
# class UserInfoSerializer(serializers.ModelSerializer):
#     xxx = serializers.CharField(source="get_user_type_display")
#     roles = serializers.SerializerMethodField()  # 自定义显示
#     # gorup = serializers.CharField(source="group.name")
#
#     class Meta:
#         model = UserInfo
#         # fields = "__all__"
#         fields = ['id', 'username', 'password', 'xxx', 'roles', 'group']
#
#     def get_roles(self, row):
#         role_obj_list = row.roles.all()
#         ret = []
#         for item in role_obj_list:
#             ret.append({'id':item.id, 'name':item.name})
#         return ret


# 方式三
class UserInfoSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedIdentityField(view_name='group', lookup_field='group_id', lookup_url_kwarg='pk')

    class Meta:
        model = UserInfo
        fields = "__all__"
        # fields = ['id', 'username', 'password', 'roles', 'group']
        depth = 1  # 官方建议0~10，尽量不要超过3层


class UserInfoView(APIView):
    """用户中心（普通用户，vip）"""
    # authentication_classes = [Authentication, ]
    # 当前permission_classes存在就不会去取配置文件里的设置
    permission_classes = [VipPermission, ]

    def get(self, request, *args, **kwargs):

        users = UserInfo.objects.all()

        # 对象（单个结果），Serializer类处理；self.to_representation
        # QuerySet，ListSerializer类处理；self.to_representation
        # 1.实例化，一般将数据封装到对象：__new__,__init__
        """
        many=True,接下来执行ListSerializer对象的构造方法
        many=False,接下来执行UserInfoSerializer对象的构造方法
        
        """
        ser = UserInfoSerializer(instance=users, many=True, context={'request': request})
        # 2.调用对象的data属性
        # ListSerializer
        # UserInfoSerializer

        # print(ser.data)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


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

# 序列化
from rest_framework import serializers


class RolesSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class RolesView(APIView):

    def get(self, request, *args, **kwargs):

        # 方式一：
        # roles = Role.objects.all().values('id', 'name')
        # roles = list(roles)
        # ret = json.dumps(roles, ensure_ascii=False)

        # 方式二：
        roles = Role.objects.all()

        # 多条数据加many属性
        ser = RolesSerializer(instance=roles, many=True)

        # 单个数据many属性为False
        # ser = Role.objects.all().first()
        # ser = RolesSerializer(instance=roles, many=False)
        # ser.data已经是转换完成的结果

        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


# 使用ModelSerializer类
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = "__all__"


class GroupView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        obj = UserGroup.objects.filter(id=pk).first()

        ser = GroupSerializer(instance=obj, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)


# 序列化数据验证
# 自定义数据校验类
class XXXValidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if not value.startswith(self.base):
            message = '名称必须以 %s 开头' % self.base
            raise serializers.ValidationError(message)


class UserGroupSerializer(serializers.Serializer):
    name = serializers.CharField(error_messages={'required': '姓名不能为空'}, validators=[XXXValidator('nzb'),])

    def validate_name(self, value):
        from rest_framework import exceptions
        # 自定义验证规则，然后抛出异常
        raise exceptions.ValidationError('看你不顺眼')
        # print(value)
        return value


class UserGroupView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):

        # print(request.data)
        ser = UserGroupSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
            # 单独取某些
            print(ser.validated_data['name'])
        else:
            print(ser.errors)
        return HttpResponse('提交数据')


#分页

from app01.utils.serializers.pager import PagerSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

# 第一种分页
# class MyPagination(PageNumberPagination):
#     # 自定义分页类
#     page_size = 2
#     page_size_query_param = 'size'
#     max_page_size = 5


# 第二种分页
# class MyPagination(LimitOffsetPagination):
#     # 自定义分页类
#     page_size = 2
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'
#     max_limit = 5

# 第三种分页
class MyPagination(CursorPagination):
    # 自定义分页类
    page_size = 2
    cursor_query_param = 'cursor'
    max_limit = 5
    ordering = 'id'
    page_size_query_param = None
    max_page_size = None


class Pager1View(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):

        # 获取所以数据
        roles = Role.objects.all()

        # ret = json.dumps(ser.data, ensure_ascii=False)
        # return HttpResponse(ret)

        # rest_framework 渲染
        # 创建分页对象
        pg = MyPagination()
        # 在数据中获取分页的数据
        pager_roles = pg.paginate_queryset(queryset=roles, request=request, view=self)
        # 对数据进行序列化
        ser = PagerSerializer(instance=pager_roles, many=True)

        # return Response(ser.data)
        # 生成上一页下一页链接(加密分页很有用)
        return pg.get_paginated_response(ser.data)


# 第三种视图
# from app01.utils.serializers.pager import PagerSerializer
# from rest_framework.generics import GenericAPIView
#
#
# class View1View(GenericAPIView):
#     queryset = Role.objects.all()
#     serializer_class = PagerSerializer
#     pagination_class = PageNumberPagination
#     authentication_classes = []
#     permission_classes = []
#
#     def get(self, request, *args, **kwargs):
#
#         # 获取数据
#         roles = self.get_queryset() # Role.objects.all()
#         # 分页 [1,100]
#         pager_roles = self.paginate_queryset(roles)
#         # 序列化
#         ser = self.get_serializer(instance=pager_roles, many=True)
#
#         return Response(ser.data)


# 第四种视图
# from app01.utils.serializers.pager import PagerSerializer
# from rest_framework.viewsets import GenericViewSet
#
#
# class View1View(GenericViewSet):
#     queryset = Role.objects.all()
#     serializer_class = PagerSerializer
#     pagination_class = PageNumberPagination
#     authentication_classes = []
#     permission_classes = []
#
#     def list(self, request, *args, **kwargs):
#
#         # 获取数据
#         roles = self.get_queryset() # Role.objects.all()
#         # 分页 [1,100]
#         pager_roles = self.paginate_queryset(roles)
#         # 序列化
#         ser = self.get_serializer(instance=pager_roles, many=True)
#
#         return Response(ser.data)


# 第五种视图
from app01.utils.serializers.pager import PagerSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

# 渲染器

from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, AdminRenderer, HTMLFormRenderer

# class View1View(ListModelMixin,GenericViewSet,CreateModelMixin):


class View1View(ModelViewSet):
    # 渲染器,使用JSONRenderer就行，BrowsableAPIRenderer只是界面好看
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    authentication_classes = []
    permission_classes = []

    queryset = Role.objects.all()
    serializer_class = PagerSerializer
    pagination_class = PageNumberPagination

