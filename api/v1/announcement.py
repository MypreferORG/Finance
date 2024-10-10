# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 14:50
# @Author : Myprefer
# @Des: 公告相关接口
"""
from typing import List

from fastapi import APIRouter

from schemas import (CreateAnnouncementRequest,
                     AnnouncementResponse,
                     UpdateAnnouncementRequest,
                     AnnouncementAbstractResponse)

router = APIRouter()


@router.post("/publish", summary="发布公告")
async def publish_announcement(announcement: CreateAnnouncementRequest):
    # 发布公告逻辑
    # todo: publish_announcement 发布公告逻辑
    pass


@router.get("/list", summary="查看公告列表", response_model=List[AnnouncementAbstractResponse])
async def list_announcements():
    # 获取公告列表逻辑
    # todo: list_announcements 获取公告列表逻辑
    pass


@router.get("/{announcement_id}", summary="查看公告", response_model=AnnouncementResponse)
async def read_announcements(announcement_id: int):
    # 查看公告逻辑
    # todo: read_announcements 查看公告逻辑
    pass


@router.post("/update", summary="更新公告")
async def update_announcement(announcement: UpdateAnnouncementRequest):
    # 更新公告逻辑
    # todo: update_announcement 更新公告逻辑
    pass


@router.delete("/delete/{announcement_id}", summary="删除公告")
async def delete_announcement(announcement_id: int):
    # 删除公告逻辑
    # todo: delete_announcement 删除公告逻辑
    pass
