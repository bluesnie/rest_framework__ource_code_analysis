from django.db import models

# Create your models here.


class UserGroup(models.Model):
    name = models.CharField(max_length=32)


# 用户认证
class UserInfo(models.Model):
    """用户表"""
    user_type = models.IntegerField(choices=((1, '普通用户'), (2, 'VIP'), (3, 'SVIP')))
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, null=True, blank=True)
    roles = models.ManyToManyField('Role')


class UserToken(models.Model):
    """token表"""
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)


class Role(models.Model):
    name = models.CharField(max_length=32)
