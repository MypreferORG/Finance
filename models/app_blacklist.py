# -*- coding: utf-8 -*-
"""
# @Create on : 11/13/25
# @Author : Jason
# @Des: 应用黑名单模型（记录被禁止的 App 名称）
"""
from tortoise import fields
from tortoise.models import Model

class AppBlacklist(Model):
    """应用黑名单表：记录被列入黑名单的应用名称"""
    id = fields.IntField(pk=True, description="主键ID")
    name = fields.CharField(max_length=100, unique=True, description="被拉黑的应用名称")
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")

    class Meta:
        table = "app_blacklist"
        indexes = [("name",)]

    def __str__(self):
        return f"AppBlacklist(id={self.id}, name={self.name})"
