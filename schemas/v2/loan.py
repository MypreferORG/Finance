# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/19 01:31
# @Author : Jason
# @Des: 
"""

from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field

class LoanRecordResponse(BaseModel):
    """
    贷款记录响应模型
    """
    id: int
    user_id: str
    amount: Decimal
    interest_rate: Decimal
    loan_term: int
    status: str
    repayment_method: str
    repayment_amount: Decimal
    usage: str
    bank_account: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PaginatedLoanRecordData(BaseModel):
    """
    分页贷款记录数据
    """
    total: int  # 总记录数
    pageNo: int  # 当前页码
    pageSize: int  # 每页数量
    records: List[LoanRecordResponse]  # 当前页的贷款记录列表

class PaginatedLoanRecordResponse(BaseModel):
    """
    带分页信息的贷款记录响应数据
    """
    success: bool  # 请求是否成功
    data: PaginatedLoanRecordData  # 分页的贷款记录数据

class UpdateLoanRecordRequest(BaseModel):
    """
    修改贷款记录的请求模型
    """
    amount: Optional[Decimal] = Field(None, description="借款金额")
    status: Optional[str] = Field(None, description="贷款状态（如：active、completed、defaulted、overdue等）")
    repayment_method: Optional[str] = Field(None, description="还款方式(等额本金/等额本息)")
    repayment_amount: Optional[Decimal] = Field(None, description="已还款金额")
    usage: Optional[str] = Field(None, description="借款用途")
    bank_account: Optional[str] = Field(None, description="收款/还款银行账户")

class CreateLoanRecordRequest(BaseModel):
    """
    新增贷款记录的请求模型
    """
    user_id: str = Field(..., description="用户的唯一ID")
    amount: Decimal = Field(..., description="借款金额")
    interest_rate: Decimal = Field(..., description="年利率")
    loan_term: int = Field(..., description="贷款期限（以月为单位）")
    repayment_method: str = Field(..., description="还款方式(等额本金/等额本息)")
    usage: str = Field(..., description="借款用途")
    bank_account: str = Field(..., description="收款银行账户")
