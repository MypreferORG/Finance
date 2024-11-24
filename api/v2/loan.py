# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 01:32
# @Author : Jason
# @Des: 
"""
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from models import LoanRecord, UserAuth, RepaymentRecord
from schemas.v2.loan import LoanRecordResponse, UpdateLoanRecordRequest, CreateLoanRecordRequest, \
    PaginatedLoanRecordResponse, PaginatedLoanRecordData

router = APIRouter()


@router.get("/records", summary="获取贷款记录", response_model=PaginatedLoanRecordResponse)
async def get_all_loan_records(
        loan_id: Optional[int] = Query(None, description="按贷款ID筛选"),
        user_id: Optional[int] = Query(None, description="按用户ID筛选"),
        amount: Optional[Decimal] = Query(None, description="按贷款金额筛选"),
        status: Optional[str] = Query(None, description="按贷款状态筛选（如：active、completed、defaulted、overdue等）"),
        repayment_method: Optional[str] = Query(None, description="按还款方式筛选(等额本金/等额本息)"),
        repayment_amount: Optional[Decimal] = Query(None, description="按已还款金额筛选"),
        loan_term: Optional[int] = Query(None, description="按贷款期限筛选（以月为单位）"),
        pageNo: int = Query(1, alias="pageNo", ge=1),  # 当前页码，默认值为1
        pageSize: int = Query(10, alias="pageSize", ge=1),  # 每页数量，默认值为10
):
    """
    获取所有贷款记录
    :param loan_id: 贷款ID筛选
    :param user_id: 用户ID筛选
    :param amount: 贷款金额筛选
    :param status: 按状态筛选
    :param repayment_method: 按还款方式筛选
    :param repayment_amount: 按已还款金额筛选
    :param loan_term: 按贷款期限筛选
    :param pageNo: 分页页码
    :param pageSize: 每页大小
    :return: 贷款记录列表
    """
    # 构建查询
    query = LoanRecord.all()

    # 根据参数筛选
    if loan_id:
        query = query.filter(id=loan_id)
    if user_id:
        query = query.filter(user_id=user_id)
    if amount:
        query = query.filter(amount=amount)
    if status:
        query = query.filter(status=status)
    if repayment_method:
        query = query.filter(repayment_method=repayment_method)
    if repayment_amount:
        query = query.filter(repayment_amount=repayment_amount)
    if loan_term:
        query = query.filter(loan_term=loan_term)

    # 获取总记录数
    total = await query.count()

    # 获取分页数据
    skip = (pageNo - 1) * pageSize
    records = await query.offset(skip).limit(pageSize)

    # 如果没有符合条件的记录，返回 404
    if not records:
        raise HTTPException(status_code=404, detail="没有找到符合条件的贷款记录")

    # 转换数据为响应模型
    record_list = [LoanRecordResponse.from_orm(record) for record in records]

    # 构建响应数据
    response_data = PaginatedLoanRecordResponse(
        success=True,
        data=PaginatedLoanRecordData(
            total=total,
            pageNo=pageNo,
            pageSize=pageSize,
            records=record_list
        )
    )
    return response_data

#
# @router.get("/records/{loan_id}", summary="获取单个贷款记录详情", response_model=PaginatedLoanRecordResponse)
# async def get_loan_record_by_id(loan_id: int):
#     """
#     获取单个贷款记录详情
#     :param loan_id: 贷款记录ID
#     :return: 贷款记录详细信息
#     """
#     # 查询单个贷款记录
#     loan_record = await LoanRecord.get_or_none(id=loan_id)
#
#     # 如果记录未找到，返回 404
#     if not loan_record:
#         raise HTTPException(status_code=404, detail="贷款记录未找到")
#
#     # 转换为响应模型
#     record = LoanRecordResponse.from_orm(loan_record)
#
#     # 返回分页格式的响应
#     response_data = PaginatedLoanRecordResponse(
#         success=True,
#         data=PaginatedLoanRecordData(
#             total=1,
#             pageNo=1,
#             pageSize=1,
#             records=[record]
#         )
#     )
#     return response_data
#

@router.put("/records/{loan_id}", summary="修改贷款记录")
async def update_loan_record(loan_id: int, request: UpdateLoanRecordRequest):
    """
    修改贷款记录
    :param loan_id: 贷款记录ID
    :param request: 修改内容
    :return: 修改结果
    """
    # 查找贷款记录
    loan_record = await LoanRecord.get_or_none(id=loan_id)

    if not loan_record:
        raise HTTPException(status_code=404, detail="贷款记录未找到")
    update_data = request.dict(exclude_unset=True)
    # 更新字段
    for field, value in update_data.items():
        # 校验金额是否大于 0
        # if field == "amount" and value <= 0:
        #     raise HTTPException(status_code=400, detail="还款金额必须大于 0")
        # 校验还款日期是否为有效日期
        # if field == "repayment_date" and value > datetime.now():
        #     raise HTTPException(status_code=400, detail="还款日期不能是未来的时间")
        # 更新字段
        setattr(loan_record, field, value)

    # 更新 updated_at 字段为当前时间
    loan_record.updated_at = datetime.utcnow()

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
    user = await UserAuth.get_or_none(index=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 创建贷款记录
    new_loan_record = await LoanRecord.create(
        id=request.id,
        user=user,
        amount=request.amount,
        interest_rate=request.interest_rate,
        loan_term=request.loan_term,
        repayment_method=request.repayment_method,
        repayment_amount=request.repayment_amount,  # 已还款金额
        # repayment_schedule=request.repayment_schedule,  # 还款计划
        usage=request.usage,
        bank_account=request.bank_account,
        status="active",  # 默认状态为 active
    )

    return {"msg": "贷款记录创建成功", "loan_id": new_loan_record.id}
