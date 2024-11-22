# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 12:59
# @Author : Myprefer
# @Des: 
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from core.dependences import admin_required
from models import Announcement
from schemas import (CreateAnnouncementRequest)
from schemas.article import PaginatedAnnouncementResponse, PaginatedAnnouncementData

router = APIRouter(dependencies=[Depends(admin_required)])


@router.post("/publish", summary="发布公告")
async def publish_announcement(announcement: CreateAnnouncementRequest):
    """
    发布公告逻辑
    :param user: 当前用户
    :param announcement: 公告详细信息
    """
    # 创建公告
    new_announcement = await Announcement.create(
        title=announcement.title,
        content=announcement.content,
        author=announcement.author,
        expiration_date=announcement.expiration_date,
        status="active",  # 默认状态为 active
    )

    return {
        "msg": "公告发布成功",
        "announcement_id": new_announcement.id
    }


@router.get("/search", summary="查看公告列表", response_model=PaginatedAnnouncementResponse)
async def list_announcements(
    pageNo: int = Query(1, alias="pageNo", ge=1),
    pageSize: int = Query(10, alias="pageSize", ge=1),
    title: Optional[str] = Query(None, alias="title"),
    status: Optional[str] = Query(None, alias="status"),
    author: Optional[str] = Query(None, alias="author"),
):
    """
    获取公告列表逻辑
    :return: announcements: 公告摘要列表
    """
    # 计算要跳过的记录数量
    skip = (pageNo - 1) * pageSize

    # 动态构建查询条件
    query = Announcement.all()
    if title:
        query = query.filter(title__icontains=title)
    if status:
        query = query.filter(status__icontains=status)
    if author:
        query = query.filter(author__icontains=author)

    # 获取符合条件的总记录数
    total_count = await query.count()

    # 获取当前页的公告数据
    announcements = await query.order_by('-publish_date').offset(skip).limit(pageSize)

    # 格式化数据并返回
    response_data = PaginatedAnnouncementResponse(
        success=True,
        data=PaginatedAnnouncementData(
            total=total_count,
            pageNo=pageNo,
            pageSize=pageSize,
            records=announcements
        )
    )
    return response_data


@router.post("/update/{announcement_id}", summary="更新公告")
async def update_announcement(
        announcement_id: int,
        announcement: CreateAnnouncementRequest
):
    """
    更新公告逻辑
    :param announcement_id:
    :param user: 当前用户
    :param announcement: 公告详细信息
    :retur
    """
    # 根据公告ID获取公告
    existing_announcement = await Announcement.get_or_none(id=announcement_id)

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

    return {"msg": "公告更新成功", "announcement_id": announcement_id}


@router.delete("/delete/{announcement_id}", summary="删除公告")
async def delete_announcement(announcement_id: int):
    """
    删除公告逻辑
    :param user: 当前用户
    :param announcement_id: 公告id
    :return
    """
    # 根据ID获取公告
    existing_announcement = await Announcement.get_or_none(id=announcement_id)

    # 如果公告不存在，抛出404错误
    if not existing_announcement:
        raise HTTPException(status_code=404, detail="公告未找到")

    # 删除公告
    await existing_announcement.delete()

    return {"msg": "公告删除成功", "announcement_id": announcement_id}
