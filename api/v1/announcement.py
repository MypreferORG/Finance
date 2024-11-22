# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 14:50
# @Author : Myprefer
# @Des: 公告相关接口
"""

from typing import List
from core.dependences import get_current_user
from fastapi import APIRouter, HTTPException, Depends, status
from models import Announcement, UserAuth
from schemas import (CreateAnnouncementRequest,
                     AnnouncementResponse,
                     UpdateAnnouncementRequest,
                     AnnouncementAbstractResponse)

router = APIRouter()


@router.get("/list", summary="查看公告列表", response_model=List[AnnouncementAbstractResponse])
async def list_announcements():
    """
    获取公告列表逻辑
    :return: announcements: 公告摘要列表
    """
    # 查询所有公告，按发布日期降序排列
    announcements = await Announcement.all().order_by('-publish_date')

    # 返回公告列表，自动转换为 Pydantic 模型格式
    return announcements


@router.get("/{announcement_id}", summary="查看公告", response_model=AnnouncementResponse)
async def read_announcements(announcement_id: int):
    """
    查看公告逻辑
    :param announcement_id: 公告id
    :return AnnouncementResponse: 公告详细信息
    """
    # 根据公告ID查询公告
    announcement = await Announcement.get_or_none(id=announcement_id)

    # 如果未找到公告，返回404错误
    if not announcement:
        raise HTTPException(status_code=404, detail="公告未找到")

    # 返回公告信息
    return announcement
