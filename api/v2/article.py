# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 12:59
# @Author : Myprefer
# @Des: 
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Query
from core.dependences import get_current_user
from models import Article, UserAuth
from schemas import CreateArticleRequest, ArticleResponse, ArticleAbstractResponse
from schemas.article import PaginatedArticleResponse, PaginatedArticleData, UpdateArticleRequest

router = APIRouter()


@router.post("/publish", summary="发布文章")
async def publish_article(
        article: CreateArticleRequest,
        user: UserAuth = Depends(get_current_user)):
    """
    文章发布逻辑
    :param user: 当前用户
    :param article: 文章详细信息
    :return
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" and user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )

    # 创建新文章记录
    new_article = await Article.create(
        title=article.title,
        content=article.content,
        author=article.author,
        cover_image=article.cover_image,
        summary=article.summary
    )

    return {
        "msg": "文章发布成功",
        "id": new_article.id
    }


@router.delete("/delete/{article_id}", summary="删除文章")
async def delete_article(
        article_id: int,
        user: UserAuth = Depends(get_current_user)):
    """
    删除文章逻辑
    :param user: 当前用户
    :param article_id: 文章详细信息
    :return
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" and user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )

    article = await Article.get_or_none(id=article_id)

    # 如果文章不存在，返回404错误
    if not article:
        raise HTTPException(status_code=404, detail="文章未找到")

    # 删除文章
    await article.delete()

    return {"msg": "文章删除成功", "article_id": article_id}


@router.get("/search", summary="查询文章列表", response_model=PaginatedArticleResponse)
async def list_articles(
    pageNo: int = Query(1, alias="pageNo", ge=1),
    pageSize: int = Query(10, alias="pageSize", ge=1),
    title: Optional[str] = Query(None, alias="title"),
    status: Optional[str] = Query(None, alias="status"),
    author: Optional[str] = Query(None, alias="author"),
    user: UserAuth = Depends(get_current_user)
):
    """
    获取文章列表逻辑
    :param user:
    :param pageNo:
    :param pageSize:
    :param title:
    :param status:
    :param author:
    :return:
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" and user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    # 计算要跳过的记录数量
    skip = (pageNo - 1) * pageSize

    # 动态构建查询条件
    query = Article.all()
    if title:
        query = query.filter(title__icontains=title)
    if status:
        query = query.filter(status__icontains=status)
    if author:
        query = query.filter(author__icontains=author)

    # 获取符合条件的总记录数
    total_count = await query.count()

    # 获取当前页的公告数据
    articles = await query.order_by('-publish_date').offset(skip).limit(pageSize)

    # 格式化数据并返回
    response_data = PaginatedArticleResponse(
        success=True,
        data=PaginatedArticleData(
            total=total_count,
            pageNo=pageNo,
            pageSize=pageSize,
            records=articles
        )
    )
    return response_data


@router.post("/update/{article_id}", summary="更新文章")
async def update_article(
        article_id: int,
        article: UpdateArticleRequest,
        user: UserAuth = Depends(get_current_user)):
    """
    更新文章逻辑
    :param article_id:
    :param article:
    :param user:
    :return:
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" and user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    # 根据公告ID获取公告
    existing_article = await Article.get_or_none(id=article_id)

    # 如果文章不存在，抛出404错误
    if not existing_article:
        raise HTTPException(status_code=404, detail="文章未找到")

    # 更新文章
    if article.title:
        existing_article.title = article.title
    if article.status:
        existing_article.status = article.status
    if article.content:
        existing_article.content = article.content
    if article.author:
        existing_article.author = article.author
    if article.cover_image:
        existing_article.cover_image = article.cover_image
    if article.summary:
        existing_article.summary = article.summary
    await existing_article.save()

    return {"msg": "文章更新成功", "article_id": article_id}


