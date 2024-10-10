# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 17:42
# @Author : Myprefer
# @Des: 客服相关schema
"""

from pydantic import BaseModel
from datetime import datetime
from typing import List


# 支持请求数据
class SupportRequest(BaseModel):
    contact_info: str


# 支持请求响应数据
class SupportResponse(BaseModel):
    request_id: int
    status: str
    submitted_at: datetime


# 支持历史响应数据
class SupportHistoryResponse(BaseModel):
    requests: List[SupportResponse]
