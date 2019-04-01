# _*_ encoding:utf-8 _*_
from django.contrib import admin
from django.urls import path,re_path, include
from app01 import views
from rest_framework import routers

# rest_framework路由
router = routers.DefaultRouter()
router.register(r'xxx', views.View1View)
router.register(r'rt', views.View1View)
# router.register(r'userinfo', views.UserInfoView)
# router.register(r'auth', views.AuthView)
# router.register(r'order', views.OrderView)
# router.register(r'parser', views.ParserView)
# router.register(r'roles', views.RolesView)
# router.register(r'group', views.GroupView)
# router.register(r'usergroup', views.UserGroupView)
# router.register(r'pager1', views.Pager1View)

# app_name = "app01"

urlpatterns = [
    # # 用户认证配置
    re_path('(?P<version>[v1|v2]+)/auth/', views.AuthView.as_view(), name='auth'),
    # # 用户中心
    # re_path('(?P<version>[v1|v2]+)/user/', views.UserInfoView.as_view(), name='user'),
    # # 订单配置
    re_path('(?P<version>[v1|v2]+)/order/', views.OrderView.as_view(), name='order'),
    # # 解析器配置
    # re_path('(?P<version>[v1|v2]+)/parser/', views.ParserView.as_view(), name='parser'),
    # # 序列化配置
    # path('roles/', views.RolesView.as_view(), name='roles'),
    # re_path('(?P<version>[v1|v2]+)/group/(?P<pk>\d+)', views.GroupView.as_view(), name='group'),
    # re_path('(?P<version>[v1|v2]+)/usergroup/', views.UserGroupView.as_view(), name='usergroup'),
    #
    # # 翻页
    # re_path('(?P<version>[v1|v2]+)/pager1/', views.Pager1View.as_view(), name='pager1'),
    # # 视图
    # # re_path('(?P<version>[v1|v2]+)/v1/', views.View1View.as_view(), name='view1'),
    #
    # # http://127.0.0.1:8000/api01/v1/v1/
    # re_path('(?P<version>[v1|v2]+)/v1/$', views.View1View.as_view({'get': 'list', 'post':'create'}), name='view1'),
    # # http://127.0.0.1:8000/api01/v1/v1.json
    # re_path('(?P<version>[v1|v2]+)/v1\.(?P<format>\w+)$', views.View1View.as_view({'get': 'list', 'post':'create'}), name='view1'),
    #
    # re_path('(?P<version>[v1|v2]+)/v1/(?P<pk>\d+)$', views.View1View.as_view({'get': 'retrieve', 'delete':'destroy', 'put': 'update', 'patch': 'partial_update'}), name='view1'),
    # re_path('(?P<version>[v1|v2]+)/v1/(?P<pk>\d+)\.(?P<format>\w+)', views.View1View.as_view({'get': 'retrieve','delete':'destroy','put': 'update','patch': 'partial_update'}), name='view1'),

    # rest_framework路由
    re_path('(?P<version>[v1|v2]+)/', include(router.urls))
]