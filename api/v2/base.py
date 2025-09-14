# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 13:07
# @Author : Myprefer
# @Des: API路由管理
"""
from fastapi import APIRouter
from api.v2 import auth, user, loan, notification, article, announcement, support, repayment, charts, model, review, decision


# 创建一个APIRouter实例，用于统一管理所有管理API
admin_api_router = APIRouter(
    prefix="/v2",
)

# 注册所有子路由
admin_api_router.include_router(auth.router, prefix="/auth", tags=["管理员登录"])
admin_api_router.include_router(user.router, prefix="/user", tags=["用户管理"])
admin_api_router.include_router(loan.router, prefix="/loan", tags=["贷款管理"])
admin_api_router.include_router(repayment.router, prefix="/repayment", tags=["还款管理"])
# admin_api_router.include_router(notification.router, prefix="/notification", tags=["通知管理"])
admin_api_router.include_router(article.router, prefix="/article", tags=["文章管理"])
admin_api_router.include_router(announcement.router, prefix="/announcement", tags=["公告管理"])
# admin_api_router.include_router(support.router, prefix="/support", tags=["客户支持"])
admin_api_router.include_router(charts.router, prefix="/charts", tags=["图表数据"])
admin_api_router.include_router(model.router, prefix="/model", tags=["模型管理"])
admin_api_router.include_router(review.router, prefix="/audit/review", tags=["复审管理"])
admin_api_router.include_router(decision.router, prefix="/decision-engine", tags=["决策引擎"])

