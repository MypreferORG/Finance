# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:35 PM
# @Author : Myprefer
# @Des: 客户支持服务(客服)接口
"""

from fastapi import APIRouter

from schemas import SupportResponse, SupportHistoryResponse, SupportRequest

router = APIRouter()


@router.post("/request", summary="提交问题", response_model=SupportResponse)
async def submit_support_request(request: SupportRequest):
    # 提交支持请求逻辑
    # todo: submit_support_request 提交支持请求逻辑
    pass


@router.get("/history", summary="查看客服聊天历史", response_model=SupportHistoryResponse)
async def support_history():
    # 获取支持历史逻辑
    # todo: support_history 获取支持历史逻辑
    pass
