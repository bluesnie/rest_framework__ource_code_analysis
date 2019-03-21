# _*_ encoding:utf-8 _*_
from django.contrib import admin
from django.urls import path,re_path
from app01 import views

# app_name = "app01"

urlpatterns = [
    # 用户认证配置
    re_path('(?P<version>[v1|v2]+)/auth/', views.AuthView.as_view(), name='auth'),
    # 用户中心
    re_path('(?P<version>[v1|v2]+)/user/', views.UserInfoView.as_view(), name='user'),
    # 订单配置
    re_path('(?P<version>[v1|v2]+)/order/', views.OrderView.as_view(), name='order'),
    # 解析器配置
    re_path('(?P<version>[v1|v2]+)/parser/', views.ParserView.as_view(), name='parser'),
    # 序列化配置
    path('roles/', views.RolesView.as_view(), name='roles'),
    re_path('(?P<version>[v1|v2]+)/group/(?P<pk>\d+)', views.GroupView.as_view(), name='group'),
    re_path('(?P<version>[v1|v2]+)/usergroup/', views.UserGroupView.as_view(), name='usergroup'),


]