# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:30 PM
# @Author : Myprefer
# @Des: 用户信息相关的schema模型
"""

from pydantic import BaseModel


# 用户个人信息数据
class UserProfile(BaseModel):
    # todo: UserProfile 用户个人信息数据
    pass


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
