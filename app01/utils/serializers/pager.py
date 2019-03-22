# _*_ encoding:utf-8 _*_

from rest_framework import serializers
from app01 import models


class PagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = "__all__"