# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 01:32
# @Author : Jason
# @Des: 
"""

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from models import LoanRecord, UserAuth, RepaymentRecord
from schemas.v2.loan import LoanRecordResponse, UpdateLoanRecordRequest, CreateLoanRecordRequest

router = APIRouter()


@router.get("/records", summary="获取所有贷款记录", response_model=List[LoanRecordResponse])
async def get_all_loan_records(
        user_id: Optional[str] = Query(None, description="按用户ID筛选"),
        status: Optional[str] = Query(None, description="按贷款状态筛选"),
        page: int = Query(1, description="分页页码"),
        limit: int = Query(10, description="分页大小")
):
    """
    获取所有贷款记录
    :param user_id: 用户ID筛选
    :param status: 按状态筛选
    :param page: 分页页码
    :param limit: 每页大小
    :return: 贷款记录列表
    """
    query = LoanRecord.all()

    # 添加筛选条件
    if user_id:
        query = query.filter(user__id=user_id)
    if status:
        query = query.filter(status=status)

    # 分页
    total = await query.count()
    records = await query.offset((page - 1) * limit).limit(limit)

    if not records:
        raise HTTPException(status_code=404, detail="没有找到符合条件的贷款记录")

    return records

@router.get("/records/{loan_id}", summary="获取单个贷款记录详情", response_model=LoanRecordResponse)
async def get_loan_record_by_id(loan_id: int):
    """
    获取单个贷款记录详情
    :param loan_id: 贷款记录ID
    :return: 贷款记录详细信息
    """
    loan_record = await LoanRecord.get_or_none(id=loan_id)

    if not loan_record:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    return loan_record

@router.put("/records/{loan_id}", summary="修改贷款记录")
async def update_loan_record(loan_id: int, request: UpdateLoanRecordRequest):
    """
    修改贷款记录
    :param loan_id: 贷款记录ID
    :param request: 修改内容
    :return: 修改结果
    """
    loan_record = await LoanRecord.get_or_none(id=loan_id)

    if not loan_record:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    # 更新字段
    for field, value in request.dict(exclude_unset=True).items():
        setattr(loan_record, field, value)

    # 保存更新后的记录
    await loan_record.save()

    return {"msg": "贷款记录修改成功", "loan_id": loan_id}

@router.delete("/records/{loan_id}", summary="删除贷款记录")
async def delete_loan_record(loan_id: int, delete_repayments: bool = Query(False, description="是否删除关联的还款记录")):
    """
    删除贷款记录
    :param loan_id: 贷款记录ID
    :param delete_repayments: 是否删除关联的还款记录
    :return: 删除结果
    """
    loan_record = await LoanRecord.get_or_none(id=loan_id)

    if not loan_record:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    # 删除关联的还款记录
    if delete_repayments:
        await RepaymentRecord.filter(loan=loan_record).delete()

    # 删除贷款记录
    await loan_record.delete()

    return {"msg": "贷款记录删除成功", "loan_id": loan_id, "delete_repayments": delete_repayments}

@router.post("/records", summary="新增贷款记录")
async def create_loan_record(request: CreateLoanRecordRequest):
    """
    新增贷款记录
    :param request: 新贷款记录的信息
    :return: 创建结果
    """
    # 检查用户是否存在
    user = await UserAuth.get_or_none(id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 创建贷款记录
    new_loan_record = await LoanRecord.create(
        user=user,
        amount=request.amount,
        interest_rate=request.interest_rate,
        loan_term=request.loan_term,
        repayment_method=request.repayment_method,
        usage=request.usage,
        bank_account=request.bank_account,
        status="active",  # 默认状态为 active
    )

    return {"msg": "贷款记录创建成功", "loan_id": new_loan_record.id}
