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


@router.post("/publish", summary="发布公告")
async def publish_announcement(
        announcement: CreateAnnouncementRequest,
        user: UserAuth = Depends(get_current_user)):
    """
    发布公告逻辑
    :param user: 当前用户
    :param announcement: 公告详细信息
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" or user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )

    # 创建公告
    new_announcement = await Announcement.create(
        title=announcement.title,
        content=announcement.content,
        author=user.username if not announcement.author else announcement.author,
        expiration_date=announcement.expiration_date,
        status="active",  # 默认状态为 active
    )

    return {
        "msg": "公告发布成功",
        "announcement_id": new_announcement.id
    }


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


@router.post("/update", summary="更新公告")
async def update_announcement(
        announcement: CreateAnnouncementRequest,
        user: UserAuth = Depends(get_current_user)):
    """
    更新公告逻辑
    :param user: 当前用户
    :param announcement: 公告详细信息
    :retur
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" or user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    # 根据公告ID获取公告
    existing_announcement = await Announcement.get_or_none(id=announcement.id)

    # 如果公告不存在，抛出404错误
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="公告未找到")

    # 更新公告字段
    if announcement.title:
        existing_announcement.title = announcement.title
    if announcement.content:
        existing_announcement.content = announcement.content
    if announcement.author:
        existing_announcement.author = announcement.author
    if announcement.expiration_date:
        existing_announcement.expiration_date = announcement.expiration_date
    if announcement.status:
        existing_announcement.status = announcement.status

    # 保存更新后的公告
    await existing_announcement.save()

    return {"msg": "公告更新成功", "announcement_id": existing_announcement.id}


@router.delete("/delete/{announcement_id}", summary="删除公告")
async def delete_announcement(
        announcement_id: int,
        user: UserAuth = Depends(get_current_user)):
    """
    删除公告逻辑
    :param user: 当前用户
    :param announcement_id: 公告id
    :return
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" or user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )

    # 根据ID获取公告
    existing_announcement = await Announcement.get_or_none(id=announcement_id)

    # 如果公告不存在，抛出404错误
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="公告未找到")

    # 删除公告
    await existing_announcement.delete()

    return {"msg": "公告删除成功", "announcement_id": announcement_id}
