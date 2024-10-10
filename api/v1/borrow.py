# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:36 PM
# @Author : Myprefer
# @Des: 借贷信息相关接口
"""
from typing import List

from fastapi import APIRouter
from schemas import BorrowQuotaResponse, BorrowInfoResponse

router = APIRouter()


@router.get("/quota", summary="查询借款额度", response_model=BorrowQuotaResponse)
async def get_borrow_quota():
    # 查询借款额度逻辑
    # todo: get_borrow_quota 查询借款额度逻辑
    pass


@router.get("/list/{status}", summary="查询不同状态的借款列表(服务中/待守约/已逾期)", response_model=List[BorrowInfoResponse])
async def borrow_status():
    # 查询借款列表状态逻辑
    # todo: borrow_status 查询借款列表状态逻辑
    pass


@router.get("/info/{borrow_id}", summary="查询借款信息", response_model=BorrowInfoResponse)
async def borrow_info(borrow_id: int):
    # 查询借款信息逻辑
    # todo: borrow_info 查询借款信息逻辑
    pass
