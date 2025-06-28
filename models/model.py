# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/26
# @Author : Myprefer
# @Des: 模型文件数据库模型
"""

from tortoise import fields
from tortoise.models import Model


class AIModel(Model):
    """模型文件信息"""
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, description="模型名称")
    version = fields.CharField(max_length=20, description="版本号")
    file_path = fields.CharField(max_length=255, description="文件路径")
    description = fields.TextField(description="模型描述")
    technical_details = fields.TextField(null=True, description="技术说明")
    file_size = fields.IntField(description="文件大小(字节)")
    file_extension = fields.CharField(max_length=10, description="文件扩展名")
    status = fields.CharField(max_length=20, default="testing", description="模型状态: active/current/testing")
    
    # 性能指标
    ks_value = fields.FloatField(null=True, description="KS值")
    bad_rate = fields.FloatField(null=True, description="坏账率")
    accuracy = fields.FloatField(null=True, description="准确率")
    recall = fields.FloatField(null=True, description="召回率")
    precision = fields.FloatField(null=True, description="精确率")
    
    # 时间字段
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "ai_models"
        indexes = [("name", "version"), ("status",)]

    def __str__(self):
        return f"AIModel(id={self.id}, name={self.name}, version={self.version}, status={self.status})"
