# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:30 PM
# @Author : Myprefer
# @Des: 用户信息相关的schema模型
"""
from datetime import date
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from fastapi import UploadFile, File


# 用户个人信息数据
class UserProfileResponse(BaseModel):
    """
    用户个人信息数据
    """
    username: str  # 唯一用户名
    full_name: Optional[str]  # 姓名
    phone_number: str  # 电话号码
    gender: Optional[str]  # 性别
    id_card_number: Optional[str]  # 身份证号
    id_card_expiry: Optional[date]  # 身份证有效期
    profession: Optional[str]  # 职业类别
    address: Optional[str]  # 住址
    date_of_birth: Optional[date]  # 出生年月
    academic_verified: bool  # 学信网认证
    bank_account: Optional[str]  # 银行卡号
    profile_picture: Optional[str]  # 头像URL
    income: Optional[Decimal]  # 月收入

    class Config:
        from_attributes = True


# 编辑用户个人信息请求
class UpdateProfileRequest(BaseModel):
    gender: Optional[str]
    bank_account: Optional[str]
    address: Optional[str]
    profession: Optional[str]
    income: Optional[Decimal]
    profile_picture: Optional[str]
    date_of_birth: Optional[date]

    class config:
        from_attributes = True


# 实名认证请求
class VerifyIdentityRequest(BaseModel):
    # 实名认证请求
    full_name: str
    id_card_number: str
    id_card_expiry: date
    # id_card_front: UploadFile = File(...)  # todo: 身份证正面照片
    # id_card_back: UploadFile = File(...)  # todo: 身份证反面照片


# 学信网认证请求
class VerifyAcademicRequest(BaseModel):
    full_name: str  # 姓名
    id_card_number: str  # 身份证号码
    school: str  # 学校名称
    student_id: str  # 学号
    # academic_report: UploadFile = File(...)  # todo: 学信网认证报告图片


# 绑定银行卡请求
class BindBankAccountRequest(BaseModel):
    bank_account: str  # 银行卡号
    phone_number: str  # 银行预留手机号
    verification_code: str  # 验证码
