# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:47 PM
# @Author : Myprefer
# @Des: 所有API接口的定义
"""

from fastapi import APIRouter
from api.v1 import announcement, article, auth, borrow, loan, notification, support, user

# 创建一个APIRouter实例，用于统一管理所有API
api_router = APIRouter()

# 注册所有子路由
api_router.include_router(auth.router, prefix="/auth", tags=["用户认证"])
api_router.include_router(user.router, prefix="/user", tags=["用户管理"])
api_router.include_router(loan.router, prefix="/loan", tags=["贷款管理"])
api_router.include_router(notification.router, prefix="/notification", tags=["通知管理"])
api_router.include_router(article.router, prefix="/article", tags=["文章管理"])
api_router.include_router(announcement.router, prefix="/announcement", tags=["公告管理"])
api_router.include_router(support.router, prefix="/support", tags=["客户支持"])
api_router.include_router(borrow.router, prefix="/borrow", tags=["借贷信息管理"])