# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/19 下午3:55
# @Author : Jason
# @Des: 
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import Field

class RepaymentRecordResponse(BaseModel):
    """
    还款记录响应模型
    """
    id: int
    loan_id: int
    user_id: str
    amount: Decimal
    repayment_date: datetime
    status: str
    message: Optional[str]

    class Config:
        orm_mode = True

class UpdateRepaymentRecordRequest(BaseModel):
    """
    修改还款记录的请求模型
    """
    amount: Optional[Decimal] = Field(None, description="还款金额")
    status: Optional[str] = Field(None, description="还款状态（如：successful、failed、overdue等）")
    message: Optional[str] = Field(None, description="备注信息")

class CreateRepaymentRecordRequest(BaseModel):
    """
    新增还款记录的请求模型
    """
    loan_id: int = Field(..., description="关联的贷款ID")
    user_id: str = Field(..., description="用户的唯一ID")
    amount: Decimal = Field(..., description="还款金额")
    status: str = Field(..., description="还款状态（如：successful、failed、overdue等）")
    message: Optional[str] = Field(None, description="备注信息")
