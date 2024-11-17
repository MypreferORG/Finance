# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:27 PM
# @Author : Myprefer
# @Des: 文章相关接口
"""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from core.dependences import get_current_user
from models import Article, UserAuth
from schemas import CreateArticleRequest, ArticleResponse, ArticleAbstractResponse

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
