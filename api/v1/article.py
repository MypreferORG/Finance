# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:27 PM
# @Author : Myprefer
# @Des: 文章相关接口
"""
from typing import List

from fastapi import APIRouter
from schemas import CreateArticleRequest, ArticleResponse, ArticleAbstractResponse

router = APIRouter()


@router.post("/publish", summary="发布文章")
async def publish_article(article: CreateArticleRequest):
    # 文章发布逻辑
    # todo: publish_article 文章发布逻辑
    pass


@router.delete("/delete/{article_id}", summary="删除文章")
async def delete_article(article_id: int):
    # 删除文章逻辑
    # todo: delete_article 删除文章逻辑
    pass


@router.get("/list", summary="查询文章列表", response_model=List[ArticleAbstractResponse])
async def list_articles():
    # 获取文章列表逻辑
    # todo: list_articles 获取文章列表逻辑
    pass


@router.get("/search/{query}", summary="搜索文章", response_model=List[ArticleAbstractResponse])
async def search_article(query: str):
    # 搜索文章逻辑
    # todo: search_article 搜索文章逻辑
    pass


@router.get("read/{article_id}", summary="查看文章", response_model=ArticleResponse)
async def read_article(article_id: int):
    # 查看文章逻辑
    # todo: read_article 查看文章逻辑
    pass
