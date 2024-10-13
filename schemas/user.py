# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:30 PM
# @Author : Myprefer
# @Des: 用户信息相关的schema模型
"""
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# 用户个人信息数据
class UserProfileResponse(BaseModel):
    # todo: UserProfileResponse 用户个人信息数据
    username: str  # 唯一用户名
    full_name: Optional[str]  # 姓名
    phone_number: str  # 电话号码
    gender: Optional[str]  # 性别
    id_card_number: Optional[str]  # 身份证号
    id_card_expiry: Optional[date]  # 身份证有效期
    profession: Optional[str]  # 职业类别
    address: Optional[str]  # 住址
    date_of_birth: Optional[date]  # 出生年月
    credit_auth: bool  # 学信网认证
    bank_account: Optional[str]  # 银行卡号
    profile_picture: Optional[str]  # 头像URL
    income: Optional[Decimal]  # 月收入

    class Config:
        orm_mode = True


# 编辑用户个人信息请求
class UpdateProfileRequest(BaseModel):
    # todo: UpdateProfileRequest 编辑用户个人信息请求
    pass


# 实名认证请求
class VerifyIdentityRequest(BaseModel):
    real_name: str
    id_card_number: str


# 学信网认证请求
class VerifyAcademicRequest(BaseModel):
    # todo: VerifyAcademicRequest 学信网认证请求
    pass
