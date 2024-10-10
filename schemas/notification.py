# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 17:04
# @Author : Myprefer
# @Des: 通知信息相关schema模型
"""

from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


# 通知消息响应数据
class Notification(BaseModel):
    title: Optional[str]
    content: str
    sent_at: datetime
    type: str


# 获取通知响应数据
class GetNotificationsResponse(BaseModel):
    notifications: List[Notification]


# 获取借款还款通知响应数据
class GetLoanNotificationsResponse(BaseModel):
    # todo: GetLoanNotificationsResponse 获取借款还款通知响应数据
    pass