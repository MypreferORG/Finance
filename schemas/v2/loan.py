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
    id: int  # 贷款记录ID
    user_id: int  # 用户ID
    amount: Decimal  # 贷款金额
    interest_rate: Decimal  # 年利率
    loan_term: int  # 贷款期限（以月为单位）
    status: str  # 贷款状态
    repayment_method: str  # 还款方式
    repayment_amount: Decimal  # 已还款金额
    usage: str  # 贷款用途
    bank_account: str  # 收款/还款银行账户
    created_at: datetime  # 贷款申请时间
    updated_at: datetime  # 贷款信息更新时间

    class Config:
        # orm_mode = True  # ORM支持
        from_attributes = True  # 支持从属性生成模型数据

class PaginatedLoanRecordData(BaseModel):
    """
    分页贷款记录数据
    """
    total: int  # 总记录数
    pageNo: int  # 当前页码
    pageSize: int  # 每页数量
    records: List[LoanRecordResponse]  # 当前页的贷款记录列表

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedLoanRecordResponse(BaseModel):
    """
    带分页信息的贷款记录响应数据
    """
    success: bool  # 请求是否成功
    data: PaginatedLoanRecordData  # 分页的贷款记录数据

    class Config:
        # orm_mode = True
        from_attributes = True


class UpdateLoanRecordRequest(BaseModel):
    """
    修改贷款记录的请求模型
    """
    amount: Optional[Decimal] = Field(None, description="借款金额")  # 可选，更新借款金额
    status: Optional[str] = Field(None, description="贷款状态（如：active、completed、defaulted、overdue等）")  # 可选，更新贷款状态
    repayment_method: Optional[str] = Field(None, description="还款方式(等额本金/等额本息)")  # 可选，更新还款方式
    repayment_amount: Optional[Decimal] = Field(None, description="已还款金额")  # 可选，更新已还款金额
    usage: Optional[str] = Field(None, description="借款用途")  # 可选，更新借款用途
    bank_account: Optional[str] = Field(None, description="收款/还款银行账户")  # 可选，更新收款或还款银行账户

    class Config:
        # orm_mode = True  # ORM支持
        from_attributes = True  # 支持从属性生成模型数据


class CreateLoanRecordRequest(BaseModel):
    """
    新增贷款记录的请求模型
    """
    id: int = Field(..., description="贷款ID") # 贷款ID
    user_id: int = Field(..., description="用户ID")  # 用户ID
    amount: Decimal = Field(..., description="借款金额")  # 借款金额
    interest_rate: Decimal = Field(..., description="年利率")  # 年利率
    loan_term: int = Field(..., description="贷款期限（以月为单位）")  # 贷款期限
    repayment_method: str = Field(..., description="还款方式(等额本金/等额本息)")  # 还款方式
    repayment_amount: Decimal = Field(0.00, description="已还款金额，默认值为0.00")  # 已还款金额
    # repayment_schedule: Optional[str] = Field(None, description="还款计划（如每期还款金额、还款日期等）")  # 还款计划
    usage: str = Field(..., description="借款用途")  # 借款用途
    bank_account: str = Field(..., description="收款银行账户")  # 收款银行账户

    class Config:
        # orm_mode = True
        from_attributes = True
