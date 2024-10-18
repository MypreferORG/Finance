# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 17:04
# @Author : Myprefer
# @Des: 通知信息相关schema模型
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# 通知消息响应数据
class NotificationResponse(BaseModel):
    title: Optional[str]
    content: str
    sent_at: datetime
    type: str

    class Config:
        from_attributes = True


# 获取借款还款通知响应数据
class LoanNotificationsResponse(BaseModel):
    # todo: LoanNotificationsResponse 获取借款还款通知响应数据
    pass