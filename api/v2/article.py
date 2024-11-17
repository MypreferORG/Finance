# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 12:59
# @Author : Myprefer
# @Des: 
"""

from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from core.dependences import get_current_user
from models import Article, UserAuth
from schemas import CreateArticleRequest, ArticleResponse, ArticleAbstractResponse

router = APIRouter()

