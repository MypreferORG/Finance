# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 用户注册、登录相关接口
"""
from typing import Union

from fastapi import APIRouter
from schemas import (RegisterRequest,
                     RegisterResponse,
                     LoginResponse,
                     LoginWithPasswordRequest,
                     LoginWithVerificationCodeRequest,
                     ForgotPasswordRequest,
                     ResetPasswordRequest)

router = APIRouter()


@router.post("/register", summary="用户注册", response_model=RegisterResponse)
async def register(user_create: RegisterRequest):
    # 注册逻辑
    # todo: register 注册逻辑
    pass


@router.post("/login", summary="用户登录", response_model=LoginResponse)
async def login(user: Union[LoginWithPasswordRequest, LoginWithVerificationCodeRequest]):
    # 登录逻辑
    # todo: login 登录逻辑
    pass


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
