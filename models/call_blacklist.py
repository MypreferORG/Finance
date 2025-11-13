# -*- coding: utf-8 -*-
"""
# @Create on : 11/13/25
# @Author : Jason
# @Des: 电话黑名单模型（记录被禁止的电话号码）
"""
from tortoise import fields
from tortoise.models import Model

class CallBlacklist(Model):
    """电话黑名单表：记录被列入黑名单的电话号码"""
    id = fields.IntField(pk=True, description="主键ID")
    phone_number = fields.CharField(max_length=20, unique=True, description="被拉黑的电话号码")
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")

    class Meta:
        table = "call_blacklist"
        indexes = [("phone_number",)]

    def __str__(self):
        return f"CallBlacklist(id={self.id}, phone_number={self.phone_number})"
