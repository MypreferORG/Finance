# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 个人信息管理相关接口
"""

from fastapi import APIRouter
from schemas import UserProfile, UpdateProfileRequest, VerifyIdentityRequest, VerifyAcademicRequest

router = APIRouter()


@router.get("/profile", summary="查看个人信息", response_model=UserProfile)
async def get_profile():
    # 获取个人信息逻辑
    # todo: get_profile 查看个人信息逻辑
    pass


@router.post("/profile/update", summary="编辑个人信息")
async def update_profile(request: UpdateProfileRequest):
    # 编辑个人信息逻辑
    # todo: update_profile 编辑个人信息逻辑
    pass


@router.post("/verify/identity", summary="实名认证")
async def verify_identity(request: VerifyIdentityRequest):
    # 实名认证逻辑
    # todo: verify_identity 实名认证逻辑
    pass


@router.post("/verify/academic", summary="学信网认证")
async def verify_identity(request: VerifyAcademicRequest):
    # 学信网认证逻辑
    # todo: verify_identity 学信网认证逻辑
    pass
