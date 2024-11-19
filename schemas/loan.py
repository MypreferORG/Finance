# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:31 PM
# @Author : Myprefer
# @Des: 贷款相关的schema模型
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel


class LoanQuotaResponse(BaseModel):
    """
    贷款额度响应数据
    """
    max_amount: Decimal  # 可贷款额度
    credit: Decimal  # 信用分数

    class Config:
        from_attributes = True


class LoanApplicationRequest(BaseModel):
    """
    贷款申请请求数据
    """
    usage: str  # 借款用途
    loan_term: int  # 贷款期限（以月为单位）
    amount: Decimal  # 借款金额
    repayment_method: int  # 还款方式(等额本金/等额本息)

    class Config:
        from_attributes = True


class LoanApplicationResponse(BaseModel):
    """
    贷款申请响应数据
    """
    id: int
    status: str
    loan_term: int
    amount: Decimal
    repayment_method: str
    created_at: datetime

    class Config:
        from_attributes = True


class LoanStatusResponse(BaseModel):
    """
    贷款状态响应数据
    """
    id: int  # 贷款记录ID
    amount: Decimal  # 借款金额
    interest_rate: Decimal  # 年利率
    loan_term: int  # 贷款期限（以月为单位）
    status: str  # 贷款状态（active, completed, defaulted, overdue等）
    repayment_method: str  # 还款方式(等额本金/等额本息)
    repayment_amount: Decimal  # 已还款金额
    usage: str  # 借款用途
    bank_account: str  # 银行账户
    created_at: datetime  # 贷款申请时间
    updated_at: datetime  # 贷款信息更新时间

    class Config:
        from_attributes = True


class RepaymentPlan(BaseModel):
    installment_number: int  # 期数
    amount_due: Decimal  # 每期应还款金额
    due_date: str  # 还款到期日期


class RepaymentPlanInfo(BaseModel):
    """
    还款计划信息
    """
    loan_id: int  # 贷款ID
    amount: Decimal  # 借款金额
    interest_rate: Decimal  # 年利率
    loan_term: int  # 贷款期限（以月为单位）
    status: str  # 贷款状态（active, completed, defaulted, overdue等）
    repayment_method: str  # 还款方式(等额本金/等额本息)
    bank_account: str  # 银行账户
    created_at: datetime  # 贷款申请时间

    class Config:
        from_attributes = True


class RepaymentPlanResponse(BaseModel):
    """
    还款计划响应数据
    """
    loan_record: RepaymentPlanInfo  # 贷款记录
    repayment_plan: List[RepaymentPlan]  # 还款计划列表

    class Config:
        from_attributes = True


class RepaymentRequest(BaseModel):
    """
    还款请求数据
    """
    loan_id: int  # 关联的贷款ID
    amount: Decimal  # 还款金额

    class Config:
        from_attributes = True


class RepaymentResponse(BaseModel):
    """
    还款响应数据
    """
    id: int  # 还款记录ID
    loan_id: int  # 关联的贷款ID
    amount: Decimal  # 还款金额
    repayment_date: datetime  # 还款时间
    status: str  # 还款状态（successful, failed, overdue等）

    class Config:
        from_attributes = True
