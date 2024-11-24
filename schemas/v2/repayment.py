# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/19 下午3:55
# @Author : Jason
# @Des: 
"""

from pydantic import BaseModel, validator
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field

class RepaymentRecordResponse(BaseModel):
    """
    还款记录响应模型
    """
    id: int
    loan_id: int
    user_id: int
    amount: Decimal
    repayment_date: datetime
    status: str
    message: Optional[str]

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedRepaymentRecordData(BaseModel):
    """
    分页还款记录数据
    """
    total: int  # 总记录数
    pageNo: int  # 当前页码
    pageSize: int  # 每页数量
    records: List[RepaymentRecordResponse]  # 当前页的还款记录列表

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedRepaymentRecordResponse(BaseModel):
    """
    带分页信息的还款记录响应数据
    """
    success: bool  # 请求是否成功
    data: PaginatedRepaymentRecordData  # 分页的还款记录数据

    class Config:
        # orm_mode = True
        from_attributes = True


class UpdateRepaymentRecordRequest(BaseModel):
    """
    修改还款记录的请求模型
    """
    amount: Optional[Decimal] = Field(None, description="还款金额")
    status: Optional[str] = Field(None, description="还款状态（如：successful、failed、overdue等）")
    message: Optional[str] = Field(None, description="备注信息")
    repayment_date: Optional[datetime] = Field(None, description="还款日期")

    class Config:
        # orm_mode = True
        from_attributes = True


class CreateRepaymentRecordRequest(BaseModel):
    """
    新增还款记录的请求模型
    """
    id: int = Field(..., description="还款ID")
    loan_id: int = Field(..., description="关联的贷款ID")
    user_id: int = Field(..., description="用户的唯一ID")
    amount: Decimal = Field(..., description="还款金额")
    repayment_date: datetime = Field(..., description="还款日期")
    status: str = Field(..., description="还款状态（如：successful、failed、overdue等）")
    message: Optional[str] = Field(None, description="备注信息")


    class Config:
        # orm_mode = True
        from_attributes = True