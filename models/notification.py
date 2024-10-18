# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 17:12
# @Author : Myprefer
# @Des: 
"""

from tortoise import fields
from tortoise.models import Model


class NotificationResponse(Model):
    """
    通知表：用于记录系统发送给用户的通知信息
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, description="通知标题")
    content = fields.TextField(description="通知内容")
    type = fields.CharField(max_length=50, description="通知类型（如：系统通知、推文通知、公告提醒等）")
    target_user = fields.ForeignKeyField("finance.UserAuth", related_name="notifications", description="接收通知的用户")
    is_read = fields.BooleanField(default=False, description="是否已读")
    created_at = fields.DatetimeField(auto_now_add=True, description="通知创建时间")
    status = fields.CharField(max_length=20, default="sent", description="通知状态（如：sent、failed）")

    class Meta:
        table = "notification"
        indexes = [("target_user", "created_at")]  # 根据用户和通知时间创建索引

    def __str__(self):
        return f"NotificationResponse(id={self.id}, title={self.title}, user={self.target_user.username}, status={self.status})"
