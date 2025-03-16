# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 12:59
# @Author : Myprefer
# @Des: 
"""
import random
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from core.dependences import admin_required
from models import Article
from schemas import CreateArticleRequest
from schemas.article import PaginatedArticleResponse, PaginatedArticleData, UpdateArticleRequest

router = APIRouter(dependencies=[Depends(admin_required)])


@router.post("/publish", summary="发布文章")
async def publish_article(article: CreateArticleRequest):
    """
    文章发布逻辑
    :param article: 文章详细信息
    :return article_id: 文章id
    """
    # 检查文章是否已存在（根据 URL）
    existing_article = await Article.get_or_none(link=article.link)
    if existing_article:
        return {
            "msg": "文章已存在",
            "id": existing_article.id
        }
    publish_date = datetime.now()
    random_months = random.randint(1, 12)
    random_days = random.randint(0, 30)
    fakeTime = publish_date - timedelta(days=random_months * 30 + random_days)
    # 创建新文章记录
    new_article = await Article.create(
        link=article.link,
        title=article.title,
        summary=article.summary,
        publish_date=fakeTime
    )

    return {
        "msg": "文章发布成功",
        "id": new_article.id
    }


@router.delete("/delete/{article_id}", summary="删除文章")
async def delete_article(article_id: int):
    """
    删除文章逻辑
    :param article_id: 文章ID
    :return article_id: 文章id
    """
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
):
    """
    获取文章列表逻辑
    :param pageNo: 页码
    :param pageSize: 每页数量
    :param title: 标题
    :return: articles: 文章摘要列表
    """
    # 计算要跳过的记录数量
    skip = (pageNo - 1) * pageSize

    # 动态构建查询条件
    query = Article.all()
    if title:
        query = query.filter(title__icontains=title)

    # 获取符合条件的总记录数
    total_count = await query.count()

    # 获取当前页的文章数据
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
        article: UpdateArticleRequest):
    """
    更新文章逻辑
    :param article_id: 文章ID
    :param article: 文章详细信息
    :return: article_id: 文章id
    """
    # 根据文章ID获取文章
    existing_article = await Article.get_or_none(id=article_id)

    # 如果文章不存在，抛出404错误
    if not existing_article:
        raise HTTPException(status_code=404, detail="文章未找到")

    # 更新文章
    if article.title:
        existing_article.title = article.title
    if article.summary:
        existing_article.summary = article.summary
    await existing_article.save()

    return {"msg": "文章更新成功", "article_id": article_id}

