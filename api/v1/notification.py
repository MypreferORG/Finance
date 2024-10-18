# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 通知与文章推送接口
"""
from typing import List
from fastapi import APIRouter
from schemas import NotificationResponse

router = APIRouter()


@router.get("/{notification_type}", summary="获取推送消息", response_model=List[NotificationResponse])
async def get_notifications(notification_type: str):
    # 获取通知逻辑
    # notification_type: 通知类别: 公告通知, 推文通知, 还款提醒
    # todo: get_notifications 获取通知逻辑
    pass


