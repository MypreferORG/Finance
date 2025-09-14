# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/27
# @Author : Myprefer
# @Des: 复审申请数据库模型
"""

from tortoise import fields
from tortoise.models import Model


class ReviewApplication(Model):
    """复审申请模型"""
    id = fields.IntField(pk=True)
    original_audit_id = fields.IntField(description="原始审核记录ID")
    applicant_name = fields.CharField(max_length=50, description="申请人姓名")
    phone = fields.CharField(max_length=20, description="联系电话")
    id_card = fields.CharField(max_length=18, description="身份证号")
    loan_amount = fields.DecimalField(max_digits=10, decimal_places=2, description="贷款金额")
    loan_purpose = fields.CharField(max_length=100, description="贷款用途")
    
    # 原始审核信息
    original_result = fields.CharField(max_length=20, description="原审核结果")
    original_reason = fields.TextField(description="原拒绝原因")
    original_auditor = fields.CharField(max_length=50, description="原审核员")
    original_audit_time = fields.DatetimeField(description="原审核时间")
    
    # 复审申请信息
    review_reason = fields.TextField(description="复审理由")
    review_apply_time = fields.DatetimeField(auto_now_add=True, description="复审申请时间")
    status = fields.CharField(max_length=20, default="review_pending", description="复审状态")
    priority = fields.CharField(max_length=10, default="medium", description="优先级")
    additional_docs = fields.JSONField(default=list, description="补充材料文件名列表")
    
    # 复审处理信息
    review_auditor = fields.CharField(max_length=50, null=True, description="复审员")
    review_time = fields.DatetimeField(null=True, description="复审时间")
    review_result = fields.CharField(max_length=20, null=True, description="复审结果")
    review_comment = fields.TextField(null=True, description="复审意见")
    
    # 时间字段
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "review_applications"
        indexes = [("status",), ("priority",), ("original_audit_id",)]

    def __str__(self):
        return f"ReviewApplication(id={self.id}, applicant_name={self.applicant_name}, status={self.status})"
