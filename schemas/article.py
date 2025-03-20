# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 17:34
# @Author : Myprefer
# @Des: 文章与公告的schema模型
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


# 文章创建请求数据
# class CreateArticleRequest(BaseModel):
#     title: str
#     content: str
#     author: str
#     cover_image: Optional[str] = None
#     summary: Optional[str] = None
#
#     class Config:
#         from_attributes = True

# 文章创建请求数据（只存储文章链接）
class CreateArticleRequest(BaseModel):
    link: HttpUrl  # 确保是合法的 URL
    title: Optional[str] = None  # 文章标题可以为空
    summary: Optional[str] = None

    class Config:
        from_attributes = True

# 更新文章请求数据
# class UpdateArticleRequest(BaseModel):
#     title: Optional[str] = None
#     content: Optional[str] = None
#     author: Optional[str] = None
#     cover_image: Optional[str] = None
#     summary: Optional[str] = None
#     status: Optional[str] = None
#
#
#     class Config:
#         from_attributes = True

# 更新文章请求数据（只允许更新标题）
class UpdateArticleRequest(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    class Config:
        from_attributes = True

# 文章响应数据
# class ArticleResponse(BaseModel):
#     id: int
#     title: str
#     author: str
#     content: str
#     cover_image: Optional[str] = None
#     summary: Optional[str] = None
#     publish_date: datetime
#     views: int
#     status: str
#
#
#     class Config:
#         from_attributes = True


# 文章响应数据
class ArticleResponse(BaseModel):
    id: int
    link: HttpUrl
    title: Optional[str] = None
    publish_date: datetime
    summary: Optional[str] = None

    class Config:
        from_attributes = True

# # 文章摘要响应数据
# class ArticleAbstractResponse(BaseModel):
#     id: int
#     title: str
#     author: str
#     cover_image: Optional[str] = None
#     summary: Optional[str] = None
#     publish_date: datetime
#
#     class Config:
#         from_attributes = True

class ArticleAbstractResponse(BaseModel):
    id: int
    link: HttpUrl  # 使用 HttpUrl 类型确保链接合法性
    title: Optional[str] = None
    summary: Optional[str] = None
    publish_date: datetime

    class Config:
        from_attributes = True

# 分页数据
class PaginatedArticleData(BaseModel):
    total: int
    pageNo: int
    pageSize: int
    records: List[ArticleResponse]


# 带分页信息的文章列表响应数据
class PaginatedArticleResponse(BaseModel):
    success: bool
    data: PaginatedArticleData


# 创建公告请求数据
class CreateAnnouncementRequest(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    expiration_date: Optional[datetime] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True


# 公告摘要响应数据
class AnnouncementAbstractResponse(BaseModel):
    """
    公告摘要响应数据
    id: 公告ID
    title: 公告标题
    publish_date: 公告发布时间
    expiration_date: 公告过期时间（可选）
    """
    id: int
    title: str
    publish_date: datetime
    expiration_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# 公告响应数据
class AnnouncementResponse(BaseModel):
    """
    公告响应数据
    """
    id: int
    title: str
    content: str
    status: str
    author: Optional[str] = None
    publish_date: datetime
    expiration_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class PaginatedAnnouncementData(BaseModel):
    """
    分页数据
    """
    total: int
    pageNo: int
    pageSize: int
    records: List[AnnouncementResponse]


class PaginatedAnnouncementResponse(BaseModel):
    """
    带分页信息的公告列表响应数据
    """
    success: bool
    data: PaginatedAnnouncementData


class UpdateAnnouncementRequest(BaseModel):
    """
    更新公告请求数据
    """
    title: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    summary: Optional[str] = None

    class Config:
        from_attributes = True
