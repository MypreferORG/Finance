# -*- coding: utf-8 -*-
"""
# @Create on : 2025/11/13
# @Author : Jason
# @Des: 黑名单相关 schema
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# App 黑名单
class AppBlacklistCreateRequest(BaseModel):
    name: str

    class Config:
        from_attributes = True

class AppBlacklistResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

# 电话黑名单
class CallBlacklistCreateRequest(BaseModel):
    phone_number: str

    class Config:
        from_attributes = True

class CallBlacklistResponse(BaseModel):
    id: int
    phone_number: str
    created_at: datetime

    class Config:
        from_attributes = True

# 通用删除响应
class DeleteSuccessResponse(BaseModel):
    success: bool
    message: str

# 列表包装
class AppBlacklistListResponse(BaseModel):
    total: int
    pageNo: int
    pageSize: int
    records: List[AppBlacklistResponse]

class CallBlacklistListResponse(BaseModel):
    total: int
    pageNo: int
    pageSize: int
    records: List[CallBlacklistResponse]

# ---------------- 检测用外部输入结构 ----------------
class AppInfoCheckRequest(BaseModel):
    """外部传入的应用信息，仅使用 name 做匹配，可扩展 pkgName 等"""
    name: str
    pkgName: Optional[str] = None
    versionName: Optional[str] = None
    versionCode: Optional[int] = None
    isSystemApp: Optional[bool] = None
    icon: Optional[str] = None  # base64，可忽略

    class Config:
        from_attributes = True

class PhoneNumberItem(BaseModel):
    value: str
    type: Optional[str] = None

class ContactInfoCheckRequest(BaseModel):
    displayName: Optional[str] = None
    phoneNumbers: List[PhoneNumberItem]

    class Config:
        from_attributes = True

# 批量应用检测请求
class AppInfoBatchCheckRequest(BaseModel):
    apps: List[AppInfoCheckRequest]

    class Config:
        from_attributes = True

# 批量联系人检测请求
class ContactInfoBatchCheckRequest(BaseModel):
    contacts: List[ContactInfoCheckRequest]

    class Config:
        from_attributes = True

