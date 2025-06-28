# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/26
# @Author : Myprefer
# @Des: 模型上传相关的Schema
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ModelUploadResponse(BaseModel):
    """模型上传响应"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="模型上传成功")
    data: Optional[dict] = Field(default=None)


class ModelInfoResponse(BaseModel):
    """模型信息响应"""
    id: int
    name: str
    version: str
    status: str
    ks_value: Optional[float] = None
    bad_rate: Optional[float] = None
    accuracy: Optional[float] = None
    recall: Optional[float] = None
    precision: Optional[float] = None
    create_time: str
    update_time: str
    description: str
    technical_details: Optional[str] = None


class ModelListResponse(BaseModel):
    """模型列表响应"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: dict


class ModelStatisticsResponse(BaseModel):
    """模型统计响应"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: dict


class ModelTrendResponse(BaseModel):
    """模型趋势响应"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: List[dict]


class ModelUpdateRequest(BaseModel):
    """模型更新请求"""
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None


class ModelMetricsRequest(BaseModel):
    """模型指标更新请求"""
    ks_value: Optional[float] = None
    bad_rate: Optional[float] = None
    accuracy: Optional[float] = None
    recall: Optional[float] = None
    precision: Optional[float] = None


class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = Field(default=True)
    code: int = Field(default=200)
    message: str = Field(default="操作成功")
    data: Optional[dict] = Field(default=None)
