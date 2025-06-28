# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/27
# @Author : Myprefer
# @Des: 复审管理相关的Schema
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ReviewApplicationResponse(BaseModel):
    """复审申请响应模型"""
    id: int
    original_audit_id: int
    applicant_name: str
    phone: str
    id_card: str
    loan_amount: Decimal
    loan_purpose: str
    original_result: str
    original_reason: str
    original_auditor: str
    original_audit_time: str
    review_reason: str
    review_apply_time: str
    status: str
    priority: str
    additional_docs: List[str]
    review_auditor: Optional[str] = None
    review_time: Optional[str] = None
    review_result: Optional[str] = None
    review_comment: Optional[str] = None


class ReviewApplicationListResponse(BaseModel):
    """复审申请列表响应模型"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: dict


class OriginalApplicationResponse(BaseModel):
    """原始申请响应模型"""
    id: int
    applicant_name: str
    phone: str
    id_card: str
    loan_amount: Decimal
    loan_purpose: str
    income: Optional[Decimal] = None
    credit_score: Optional[int] = None
    apply_time: str
    status: str
    audit_time: Optional[str] = None
    auditor: Optional[str] = None
    remark: Optional[str] = None


class ReviewApplicationDetailResponse(BaseModel):
    """复审申请详情响应模型"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: dict


class ReviewProcessRequest(BaseModel):
    """复审处理请求模型"""
    result: str = Field(..., description="审批结果：approved/rejected")
    comment: str = Field(..., min_length=10, max_length=500, description="审批意见")
    auditor: str = Field(..., description="审核员姓名")

    @validator('result')
    def validate_result(cls, v):
        if v not in ['approved', 'rejected']:
            raise ValueError('审批结果必须是 approved 或 rejected')
        return v


class BatchReviewProcessRequest(BaseModel):
    """批量复审处理请求模型"""
    ids: List[int] = Field(..., description="复审申请ID数组")
    result: str = Field(..., description="审批结果：approved/rejected")
    comment: str = Field(..., min_length=10, max_length=500, description="审批意见")
    auditor: str = Field(..., description="审核员姓名")

    @validator('result')
    def validate_result(cls, v):
        if v not in ['approved', 'rejected']:
            raise ValueError('审批结果必须是 approved 或 rejected')
        return v

    @validator('ids')
    def validate_ids(cls, v):
        if not v or len(v) == 0:
            raise ValueError('ID数组不能为空')
        return v


class ReviewStatsResponse(BaseModel):
    """复审统计响应模型"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: dict


class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: Optional[dict] = Field(default=None)


class ReviewHistoryResponse(BaseModel):
    """复审历史记录响应模型"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: dict
