# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/19 下午3:55
# @Author : Jason
# @Des: 
"""
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from models import RepaymentRecord, LoanRecord, UserAuth
from schemas.v2.repayment import RepaymentRecordResponse, UpdateRepaymentRecordRequest, CreateRepaymentRecordRequest, \
    PaginatedRepaymentRecordResponse, PaginatedRepaymentRecordData

router = APIRouter()


@router.get("/records", summary="获取还款记录", response_model=PaginatedRepaymentRecordResponse)
async def get_all_repayment_records(
        repayment_id: Optional[int] = Query(None, description="按还款ID筛选"),
        loan_id: Optional[int] = Query(None, description="按贷款ID筛选"),
        user_id: Optional[str] = Query(None, description="按用户ID筛选"),
        status: Optional[str] = Query(None, description="还款状态（如：successful、failed、overdue等）"),
        min_amount: Optional[Decimal] = Query(None, description="还款金额下限"),
        max_amount: Optional[Decimal] = Query(None, description="还款金额上限"),
        start_date: Optional[datetime] = Query(None, description="还款开始时间"),
        end_date: Optional[datetime] = Query(None, description="还款结束时间"),
        pageNo: int = Query(1, alias="pageNo", ge=1),
        pageSize: int = Query(10, alias="pageSize", ge=1),
):
    """
    获取所有还款记录
    :param loan_id: 贷款ID筛选
    :param user_id: 用户ID筛选
    :param status: 按状态筛选
    :param min_amount: 还款金额下限筛选
    :param max_amount: 还款金额上限筛选
    :param start_date: 还款开始时间筛选
    :param end_date: 还款结束时间筛选
    :param pageNo: 分页页码
    :param pageSize: 每页大小
    :return: 还款记录列表
    """
    # 构建查询
    query = RepaymentRecord.all()
    if repayment_id:
        query = query.filter(id=repayment_id)
    if loan_id:
        query = query.filter(loan_id=loan_id)
    if user_id:
        query = query.filter(user_id=user_id)
    if status:
        query = query.filter(status=status)
    if min_amount is not None:
        query = query.filter(amount__gte=min_amount)
    if max_amount is not None:
        query = query.filter(amount__lte=max_amount)
    if start_date is not None:
        query = query.filter(repayment_date__gte=start_date)
    if end_date is not None:
        query = query.filter(repayment_date__lte=end_date)

    # 获取总记录数
    total = await query.count()

    # 获取分页数据
    skip = (pageNo - 1) * pageSize
    records = await query.offset(skip).limit(pageSize)

    # 如果没有数据，返回 404
    if not records:
        raise HTTPException(status_code=400, detail="没有找到符合条件的还款记录")

    # 转换数据为响应模型
    record_list = records

    # 构建响应数据
    response_data = PaginatedRepaymentRecordResponse(
        success=True,
        data=PaginatedRepaymentRecordData(
            total=total,
            pageNo=pageNo,
            pageSize=pageSize,
            records=record_list
        )
    )
    return response_data


# @router.get("/records/{repayment_id}", summary="获取单个还款记录详情", response_model=PaginatedRepaymentRecordResponse)
# async def get_repayment_record_by_id(repayment_id: int):
#     """
#     获取单个还款记录详情
#     :param repayment_id: 还款记录ID
#     :return: 还款记录详细信息
#     """
#     # 查询单个还款记录
#     repayment_record = await RepaymentRecord.get_or_none(id=repayment_id)
#
#     # 如果记录未找到，返回 404
#     if not repayment_record:
#         raise HTTPException(status_code=404, detail="还款记录未找到")
#
#     # 转换为响应模型
#     record = RepaymentRecordResponse.from_orm(repayment_record)
#
#     # 返回分页格式的响应
#     response_data = PaginatedRepaymentRecordResponse(
#         success=True,
#         data=PaginatedRepaymentRecordData(
#             total=1,
#             pageNo=1,
#             pageSize=1,
#             records=[record]
#         )
#     )
#     return response_data
#

@router.put("/records/{repayment_id}", summary="修改还款记录")
async def update_repayment_record(repayment_id: int, request: UpdateRepaymentRecordRequest):
    """
    修改还款记录
    :param repayment_id: 还款记录ID
    :param request: 修改内容
    :return: 修改结果
    """
    # 检查还款记录是否存在
    repayment_record = await RepaymentRecord.get_or_none(id=repayment_id)
    if not repayment_record:
        raise HTTPException(status_code=404, detail=f"还款记录未找到: repayment_id={repayment_id}")

    # 获取请求中的更新内容，排除未设置的字段
    update_data = request.dict(exclude_unset=True)

    # 执行字段更新
    for field, value in update_data.items():
        # 校验金额是否大于 0
        if field == "amount" and value <= 0:
            raise HTTPException(status_code=400, detail="还款金额必须大于 0")
        # 校验还款日期是否为有效日期
        # if field == "repayment_date" and value > datetime.now():
        #     raise HTTPException(status_code=400, detail="还款日期不能是未来的时间")
        # 更新字段
        setattr(repayment_record, field, value)

    # 保存更新后的记录
    await repayment_record.save()

    return {
        "msg": "还款记录修改成功",
        "repayment_id": repayment_id,
        "updated_fields": update_data,
    }



@router.delete("/records/{repayment_id}", summary="删除还款记录")
async def delete_repayment_record(repayment_id: int):
    """
    删除还款记录
    :param repayment_id: 还款记录ID
    :return: 删除结果
    """
    repayment_record = await RepaymentRecord.get_or_none(id=repayment_id)

    if not repayment_record:
        raise HTTPException(status_code=404, detail="还款记录未找到")

    # 删除还款记录
    await repayment_record.delete()

    return {"msg": "还款记录删除成功", "repayment_id": repayment_id}

@router.post("/records", summary="新增还款记录")
async def create_repayment_record(request: CreateRepaymentRecordRequest):
    """
    新增还款记录
    :param request: 新还款记录的信息
    :return: 创建结果
    """
    # 检查贷款记录是否存在
    loan = await LoanRecord.get_or_none(id=request.loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    # 检查用户是否存在
    user = await UserAuth.get_or_none(index=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 创建还款记录
    new_repayment_record = await RepaymentRecord.create(
        id=request.id,
        loan=loan,
        user=user,
        amount=request.amount,
        repayment_date=request.repayment_date,
        status=request.status,
        message=request.message,
    )

    return {"msg": "还款记录创建成功", "repayment_id": new_repayment_record.id}
