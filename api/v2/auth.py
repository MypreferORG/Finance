# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/13 12:53
# @Author : Myprefer
# @Des: 管理员登录
"""

import re
from datetime import timedelta
from fastapi import APIRouter, HTTPException, Request
from config import settings
from core.Auth import verify_password, create_access_token
from db.redis import sys_cache
from models import UserAuth, UserSignLog
from schemas import (LoginResponse,
                     LoginWithPasswordRequest)

router = APIRouter()


@router.post("/login", summary="管理员登录", response_model=LoginResponse)
async def login(request: Request, body: LoginWithPasswordRequest):
    """
    登录逻辑
    :param request: Request 请求对象
    :param body: LoginWithPasswordRequest 登录请求体
    :return: LoginResponse 登录响应体
    """
    # 使用用户名(电话号码)和密码进行登录
    if re.match(r'^\d{11}$', body.username):
        user = await UserAuth.get_or_none(phone_number=body.username)
    else:
        user = await UserAuth.get_or_none(username=body.username)

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")

    # 验证用户是否为管理员
    if user.role != "admin" and user.role != "root":
        raise HTTPException(status_code=400, detail="用户权限不足")

    # 生成JWT token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

    # 将JWT token存储到Redis
    cache = await sys_cache()
    await cache.set(f"jwt:{user.id}", access_token, ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    # 记录登录日志
    await UserSignLog.create(user=user,
                             action="login",
                             ip_address=request.headers.get("X-Forwarded-For", ""),
                             user_agent=request.headers.get("user-agent", ""), )

    return LoginResponse(access_token=access_token)
