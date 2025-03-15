# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:27 PM
# @Author : Myprefer
# @Des: 文章相关接口
"""

from datetime import datetime
from decimal import Decimal
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from models import Article
from models.user import UserProfile, UserApplication, UserBehavior
from schemas import ArticleResponse, ArticleAbstractResponse
from core.dependences import user_required, UserAuth
from services.passage_service import get_user_info, get_recommend_articles

router = APIRouter()


@router.get("/list", summary="查询文章列表", response_model=List[ArticleAbstractResponse])
async def list_articles():
    """
    获取文章列表逻辑
    """
    # todo: list_articles 获取文章推荐列表逻辑
    articles = await Article.all().order_by('-publish_date').limit(20)
    return articles

@router.get("/search/{query}", summary="搜索文章", response_model=List[ArticleAbstractResponse])
async def search_article(query: str):
    """
    搜索文章逻辑
    :param query: 搜索关键词
    :return articles 搜索到的文章摘要列表
    """
    # 使用包含查询字符串的方式查询文章
    # articles = await Article.filter(
    #     title__icontains=query | content__icontains=query  # 查询标题或内容中包含关键词的文章
    # ).order_by('-publish_date')

    all_articles = await Article.all()
    articles = [article for article in all_articles if
                query.lower() in article.title.lower() or query.lower() in article.content.lower()]
    articles = sorted(articles, key=lambda x: x.publish_date, reverse=True)

    return articles  # 返回匹配的文章摘要信息


@router.get("/read/{article_id}", summary="查看文章", response_model=ArticleResponse)
async def read_article(article_id: int):
    """
    查看文章逻辑
    :param article_id:
    """
    article = await Article.get_or_none(id=article_id)

    if not article:
        raise HTTPException(status_code=404, detail="文章未找到")

    return article


@router.get("/recommend", summary="推荐文章")
async def recommend_articles(
        user: UserAuth = Depends(user_required)
):
    """
    todo:推荐文章逻辑
    """
    # 获取用户信息
    user_profile = await UserProfile.get_or_none(user=user)
    user_application = await UserApplication.get_or_none(user=user)
    user_behavior = await UserBehavior.get_or_none(user=user)

    user_info = get_user_info(user_profile, user_application, user_behavior)

    if not user_info:
        raise HTTPException(status_code=500, detail="获取用户信息失败")
    
    # 获取推荐文章
    articles = get_recommend_articles(user_info)
    if not articles:
        raise HTTPException(status_code=500, detail="推荐文章失败")
    print(articles)
    return articles