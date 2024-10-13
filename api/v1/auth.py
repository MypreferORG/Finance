# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 用户注册、登录相关接口
"""

import re
from datetime import timedelta
from typing import Union
from fastapi import APIRouter, HTTPException, Request
from config import settings
from db.redis import sys_cache
from models import UserAuth, UserProfile, UserSignLog, UserApplication, UserBehavior
from core.Auth import verify_password, create_access_token, get_password_hash
from utils import random_str
from schemas import (RegisterRequest,
                     RegisterResponse,
                     LoginResponse,
                     LoginWithPasswordRequest,
                     LoginWithVerificationCodeRequest,
                     ForgotPasswordRequest,
                     ResetPasswordRequest)

router = APIRouter()


@router.post("/register", summary="用户注册", response_model=RegisterResponse)
async def register(request: Request, body: RegisterRequest):
    """
    注册逻辑
    :param request: Request
    :param body: RegisterRequest
    :return: RegisterResponse
    """
    # 检查用户名和电话号码是否可用
    existing_user = await UserAuth.get_or_none(username=body.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    existing_number = await UserAuth.get_or_none(phone_number=body.phone_number)
    if existing_number:
        raise HTTPException(status_code=400, detail="该电话号码已注册")

    # todo: 注册时检查验证码
    is_verified = True

    if not is_verified:
        raise HTTPException(status_code=400, detail="验证码错误")

    # 创建新用户
    user = await UserAuth.create(
        id=random_str(),
        username=body.username,
        phone_number=body.phone_number,
        hashed_password=get_password_hash(body.password)  # 加密密码
    )
    await UserProfile.create(user=user, phone_number=body.phone_number, username=body.username)
    await UserApplication.create(user=user)
    await UserBehavior.create(user=user)

    # 生成JWT token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)

    # 将JWT token存储到Redis
    cache = await sys_cache()
    await cache.set(f"jwt:{user.id}", access_token, ex=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)

    # 记录注册日志
    await UserSignLog.create(user=user,
                             action="register",
                             ip_address=request.headers.get("X-Forwarded-For", ""),
                             user_agent=request.headers.get("user-agent", ""), )

    return RegisterResponse(access_token=access_token)


@router.post("/login", summary="用户登录", response_model=LoginResponse)
async def login(request: Request, body: Union[LoginWithPasswordRequest, LoginWithVerificationCodeRequest]):
    """
    登录逻辑
    :param request: Request
    :param body: LoginWithPasswordRequest 或 LoginWithVerificationCodeRequest
    :return: LoginResponse
    """
    if isinstance(body, LoginWithPasswordRequest):
        # 使用用户名(电话号码)和密码进行登录
        if re.match(r'^\d{11}$', body.username):
            user = await UserAuth.get_or_none(phone_number=body.username)
        else:
            user = await UserAuth.get_or_none(username=body.username)

        if not user or not verify_password(body.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="用户名或密码错误")

    elif isinstance(body, LoginWithVerificationCodeRequest):
        # 使用手机号和验证码进行登录
        # todo: (登录时)这里应该有验证验证码的逻辑，例如从数据库或缓存中验证
        is_verified = True

        if not is_verified:
            raise HTTPException(status_code=400, detail="验证码错误或已过期")

        user = await UserAuth.get_or_none(phone=body.phone_number)
        if not user:
            raise HTTPException(status_code=400, detail="手机号未注册")

    else:
        raise HTTPException(status_code=400, detail="Bad Request")

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


@router.post("/forgot-password", summary="找回密码")
async def forgot_password(request: ForgotPasswordRequest):
    # 找回密码逻辑
    # todo: forgot_password 找回密码逻辑
    pass


@router.post("/reset-password", summary="重置密码")
async def reset_password(request: ResetPasswordRequest):
    # 重置密码逻辑
    # todo: reset_password 重置密码逻辑
    pass
