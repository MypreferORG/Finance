# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 13:09
# @Author : Myprefer
# @Des: 
"""

from fastapi import APIRouter

from api.v1 import auth, user, loan, notification, article, announcement, support

# 创建一个APIRouter实例，用于统一管理所有用户API
user_api_router = APIRouter(
    prefix="/v1",
)

# 注册所有子路由
user_api_router.include_router(auth.router, prefix="/auth", tags=["用户认证"])
user_api_router.include_router(user.router, prefix="/user", tags=["用户信息"])
user_api_router.include_router(loan.router, prefix="/loan", tags=["贷款功能"])
user_api_router.include_router(
    notification.router, prefix="/notification", tags=["通知功能"])
user_api_router.include_router(
    article.router, prefix="/article", tags=["文章功能"])
user_api_router.include_router(
    announcement.router, prefix="/announcement", tags=["公告功能"])
user_api_router.include_router(
    support.router, prefix="/support", tags=["客服功能"])
