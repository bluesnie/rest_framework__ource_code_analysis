from django.db import models

# Create your models here.


# 用户认证
class UserInfo(models.Model):
    """用户表"""
    user_type = models.IntegerField(choices=((1, '普通用户'), (2, 'VIP'), (3, 'SVIP')))
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)


class UserToken(models.Model):
    """token表"""
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
