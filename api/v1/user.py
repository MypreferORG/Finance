# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 个人信息管理相关接口
"""

from fastapi import APIRouter, Depends, HTTPException
from models import UserAuth, UserProfile
from schemas import UserProfileResponse, UpdateProfileRequest, VerifyIdentityRequest, VerifyAcademicRequest
from core.dependences import get_current_user

router = APIRouter()


@router.get("/profile", summary="查看个人信息", response_model=UserProfileResponse)
async def get_profile(user: UserAuth = Depends(get_current_user)):
    """
    查看个人信息逻辑
    :param user: UserAuth
    :return: user_profile: UserProfileResponse
    """
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    user_profile = await UserProfile.get_or_none(user=user)

    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")
    # print(user_profile.id)
    return user_profile


@router.post("/profile/update", summary="编辑个人信息")
async def update_profile(request: UpdateProfileRequest):
    # 编辑个人信息逻辑
    # todo: update_profile 编辑个人信息逻辑
    pass


@router.post("/bind/identity", summary="实名认证")
async def bind_identity(request: VerifyIdentityRequest):
    # 实名认证逻辑
    # todo: verify_identity 实名认证逻辑
    pass


@router.post("/bind/academic", summary="学信网认证")
async def bind_identity(request: VerifyAcademicRequest):
    # 学信网认证逻辑
    # todo: verify_identity 学信网认证逻辑
    pass


@router.post("/bind/bank-account", summary="绑定银行卡")
async def bind_bankcard():
    # 银行卡绑定逻辑
    # todo: bind_bankcard 银行卡绑定逻辑
    pass


@router.post("/bind/phone", summary="换绑手机号")
async def bind_phone():
    # 手机号换绑逻辑
    # todo: bind_phone 手机号换绑逻辑
    pass



