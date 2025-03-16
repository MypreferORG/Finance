# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:27 PM
# @Author : Myprefer
# @Des: 文章相关接口
"""
import random
from datetime import datetime, timedelta
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
async def list_articles(user: UserAuth = Depends(user_required)):
    """
    获取文章列表逻辑
    """
    # 获取当前用户推荐的文章
    user_recommended_articles = await user.recommended_articles.all().order_by('-publish_date').limit(20)

    return user_recommended_articles

# @router.get("/search/{query}", summary="搜索文章", response_model=List[ArticleAbstractResponse])
# async def search_article(query: str):
#     """
#     搜索文章逻辑
#     :param query: 搜索关键词
#     :return articles 搜索到的文章摘要列表
#     """
#     # 使用包含查询字符串的方式查询文章
#     # articles = await Article.filter(
#     #     title__icontains=query | content__icontains=query  # 查询标题或内容中包含关键词的文章
#     # ).order_by('-publish_date')
#
#     all_articles = await Article.all()
#     articles = [article for article in all_articles if
#                 query.lower() in article.title.lower() or query.lower() in article.content.lower()]
#     articles = sorted(articles, key=lambda x: x.publish_date, reverse=True)
#
#     return articles  # 返回匹配的文章摘要信息

@router.get("/search/{query}", summary="搜索文章", response_model=List[ArticleAbstractResponse])
async def search_article(query: str):
    """
    搜索文章逻辑
    :param query: 搜索关键词
    :return articles 搜索到的文章摘要列表
    """
    # 使用数据库查询优化搜索逻辑
    articles = await Article.filter(
        title__icontains=query  # 搜索标题中包含关键词的文章
    ).order_by('-publish_date').limit(20)

    if not articles:
        raise HTTPException(status_code=404, detail="未找到相关文章")

    return articles


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

# @router.get("/recommend", summary="推荐文章")
# async def recommend_articles(
#         user: UserAuth = Depends(user_required)
# ):
#     """
#     """
#     # 获取用户信息
#     user_profile = await UserProfile.get_or_none(user=user)
#     user_application = await UserApplication.get_or_none(user=user)
#     user_behavior = await UserBehavior.get_or_none(user=user)
#
#     user_info = get_user_info(user_profile, user_application, user_behavior)
#
#     if not user_info:
#         raise HTTPException(status_code=500, detail="获取用户信息失败")
#
#     # 获取推荐文章
#     articles = get_recommend_articles(user_info)
#     if not articles:
#         raise HTTPException(status_code=500, detail="推荐文章失败")
#     print(articles)
#     return articles


@router.get("/recommend", summary="推荐文章")
async def recommend_articles(
        user: UserAuth = Depends(user_required)
):
    """
    推荐文章逻辑
    """
    # 获取用户信息
    user_profile = await UserProfile.get_or_none(user=user)
    user_application = await UserApplication.get_or_none(user=user)
    user_behavior = await UserBehavior.get_or_none(user=user)

    user_info = get_user_info(user_profile, user_application, user_behavior)

    if not user_info:
        raise HTTPException(status_code=500, detail="获取用户信息失败")

    # 获取推荐文章
    recommended_articles_data = get_recommend_articles(user_info)
    if not recommended_articles_data:
        raise HTTPException(status_code=500, detail="推荐文章失败")

    recommended_articles = []
    for article_data in recommended_articles_data:
        # 检查文章是否已存在
        article = await Article.get_or_none(link=article_data["url"])
        if not article:
            publish_date = datetime.now()
            random_months = random.randint(1, 12)
            random_days = random.randint(0,30)
            fakeTime = publish_date - timedelta(days=random_months*30+random_days)
            # 如果文章不存在，创建文章
            article = await Article.create(
                link=article_data["url"],
                title=article_data.get("title"),
                summary=article_data.get("summary"),
                publish_date=fakeTime  # 假设推荐文章的发布时间为当前时间减去一个月到一年
            )
        # 绑定用户与文章
        await user.recommended_articles.add(article)
        recommended_articles.append(article)

    return recommended_articles
