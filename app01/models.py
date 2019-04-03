# _*_ encoding:utf-8 _*_
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.contrib.contenttypes.models import ContentType

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


# 利用content-type实现一表对应多表

class Course(models.Model):
    """
    普通课程
    """
    name = models.CharField(max_length=32)

    # 仅用于反向查找
    price_policy_list = GenericRelation('PricePolicy')


class DegreeCourse(models.Model):
    """
    学位课程
    """
    name = models.CharField(max_length=32)
    # 仅用于反向查找
    price_policy_list = GenericRelation('PricePolicy')


class PricePolicy(models.Model):
    """价格策略"""
    price = models.IntegerField()
    period = models.IntegerField()

    # 自定义
    # table_name = models.CharField(verbose_name=u'关联的表名称')
    # object_id = models.CharField(verbose_name=u'关联表中的数据id')

    # 使用Django的组件content-type
    content_type = models.ForeignKey(ContentType, verbose_name=u'关联普通可或学位课表', on_delete=models.CASCADE)  # 11、12就是上面两个表
    object_id = models.IntegerField(verbose_name=u'关联表中的数据id')

    # 帮助你快速实现content-type操作
    content_object = GenericForeignKey('content_type', 'object_id')

# 插入一条价格策略,为学位课“Python”添加一个价格策略：一个月9.9

# # 1、最基本的操作
# obj = DegreeCourse.objects.filter(name='Python').first()
# # obj.id
# cobj = ContentType.objects.filter(model='degreecourse').first()
# # cobj.id
# PricePolicy.objects.create(price=9.9, period=30, table_name_id=cobj.id, object_id=obj.id)


# 2、加一个字段后，使用content-type
# obj = DegreeCourse.objects.filter(name='Python').first()
# PricePolicy.objects.create(price=9.9, period=30, content_object=obj)

# 3、根据课程ID找到课程，并获取所有的价格策略
# course = DegreeCourse.objects.filter(id=1).first()
# price_policy = course.price_policy_list.all()
