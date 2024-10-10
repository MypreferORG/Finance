# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 15:21
# @Author : Myprefer
# @Des: 用户授权登录所需schema模型
"""

from pydantic import BaseModel


# 注册请求数据
class RegisterRequest(BaseModel):
    username: str
    password: str
    phone_number: str
    verification_code: str


# 注册响应数据（包含JWT token）
class RegisterResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 密码登录请求数据
class LoginWithPasswordRequest(BaseModel):
    username: str  # 用户名或电话号码
    password: str


# 验证码登录请求数据
class LoginWithVerificationCodeRequest(BaseModel):
    phone_number: str
    verification_code: str


# 登录响应数据（包含JWT token）
class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 找回密码请求数据
class ForgotPasswordRequest(BaseModel):
    phone_number: str


# 重置密码请求数据
class ResetPasswordRequest(BaseModel):
    verification_code: str
    new_password: str
