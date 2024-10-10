# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 17:34
# @Author : Myprefer
# @Des: 文章与公告的schema模型
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 文章创建请求数据
class CreateArticleRequest(BaseModel):
    title: str
    content: str
    author: str
    cover_image: Optional[str] = None
    summary: Optional[str] = None


# 文章响应数据
class ArticleResponse(BaseModel):
    id: int
    title: str
    author: str
    content: str
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    publish_date: datetime


# 文章摘要响应数据
class ArticleAbstractResponse(BaseModel):
    id: int
    title: str
    author: str
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    publish_date: datetime


# 创建公告请求数据
class CreateAnnouncementRequest(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    expiration_date: Optional[datetime] = None


# 公告摘要响应数据
class AnnouncementAbstractResponse(BaseModel):
    id: int
    title: str
    publish_date: datetime
    expiration_date: Optional[datetime] = None


# 公告响应数据
class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    author: Optional[str] = None
    publish_date: datetime
    expiration_date: Optional[datetime] = None


# 更新公告请求数据
class UpdateAnnouncementRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    summary: Optional[str] = None