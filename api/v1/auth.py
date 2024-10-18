# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 用户注册、登录相关接口
"""

import re
from datetime import timedelta
import random
from typing import Union
from fastapi import APIRouter, HTTPException, Request
from config import settings
from db.redis import sys_cache
from models import UserAuth, UserProfile, UserSignLog, UserApplication, UserBehavior
from core.Auth import verify_password, create_access_token, get_password_hash
from schemas.auth import SendVerificationCodeRequest
from services.sms_service import generate_and_send_code, verify_sms_code
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

    # 注册时检查验证码 todo: 验证码逻辑
    # is_verified = verify_sms_code(body.verification_code, body.phone_number)
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

        # 验证验证码 todo: 验证码逻辑
        # is_verified = verify_sms_code(body.verification_code, body.phone_number)
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
    """
    找回密码逻辑
    :param request: 手机号的找回密码请求:
    """
    # 检查手机号是否存在于用户表中
    user = await UserAuth.get_or_none(phone_number=request.phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="该手机号未注册")

    # 生成并发送验证码给用户 todo: 发送验证码
    # await generate_and_send_code(request.phone_number)

    return {"msg": "验证码已发送"}


@router.post("/reset-password", summary="重置密码")
async def reset_password(request: Request, body: ResetPasswordRequest):
    """
    重置密码逻辑
    :param body: 包含验证码和新密码的重置密码请求
    :param request:
    :return:
    """
    # 从 Redis 中获取存储的验证码并验证
    # is_verified = verify_sms_code(body.verification_code, body.phone_number)
    is_verified = True

    if not is_verified:
        raise HTTPException(status_code=400, detail="验证码错误或已过期")

    # 查找用户
    user = await UserAuth.get_or_none(phone_number=body.phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新用户密码
    hashed_password = get_password_hash(body.new_password)
    user.hashed_password = hashed_password
    await user.save()

    # 记录修改密码日志
    await UserSignLog.create(user=user,
                             action="login",
                             ip_address=request.headers.get("X-Forwarded-For", ""),
                             user_agent=request.headers.get("user-agent", ""), )


@router.post("/send-verification-code", summary="发送验证码")
async def send_verification_code(request: SendVerificationCodeRequest):
    """
    发送验证码逻辑
    :param request: 包含手机号和验证码类型的请求
    :return:
    """
    if request.code_type not in ["register", "login", "forgot-password", "reset-password"]:
        raise HTTPException(status_code=400, detail="验证码类型错误")
    await generate_and_send_code(request.phone_number)
    return {"msg": "验证码已发送"}
