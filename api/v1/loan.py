# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 贷款业务管理接口
"""

from fastapi import APIRouter
from schemas import (LoanApplicationResponse,
                     LoanApplicationRequest,
                     LoanStatusResponse,
                     RepaymentPlanResponse,
                     RepaymentRequest)

router = APIRouter()


@router.post("/apply", summary="申请贷款", response_model=LoanApplicationResponse)
async def apply_loan(request: LoanApplicationRequest):
    # 贷款申请逻辑
    # todo: apply_loan 贷款申请逻辑
    pass


@router.get("/status/{loan_id}", summary="查询贷款状态", response_model=LoanStatusResponse)
async def loan_status(loan_id: int):
    # 查询贷款状态逻辑
    # todo: loan_status 查询贷款状态逻辑
    pass


@router.get("/repayment-plan", summary="还款计划", response_model=RepaymentPlanResponse)
async def repayment_plan():
    # 生成还款计划逻辑
    # todo: repayment_plan 生成还款计划逻辑
    pass


@router.post("/repayment", summary="还款")
async def repayment(request: RepaymentRequest):
    # 还款逻辑
    # todo: repayment 还款逻辑
    pass

