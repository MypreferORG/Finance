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
from schemas.user import BindBankAccountRequest
from utils.id_card import is_valid_id_card

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


@router.post("/profile/update", summary="编辑个人信息", response_model=UserProfileResponse)
async def update_profile(request: UpdateProfileRequest, user: UserAuth = Depends(get_current_user)):
    """
    更新用户个人信息
    :param request:
    :param user:
    :return:
    """
    # 查询用户
    user_profile = await UserProfile.get_or_none(user=user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新用户个人信息
    update_fields = request.dict(exclude_unset=True)
    # 过滤掉空字符串和仅包含空白字符的字段
    update_fields = {
        key: value
        for key, value in update_fields.items()
        if value and (not isinstance(value, str) or value.strip())
    }
    for field in update_fields:
        setattr(user_profile, field, update_fields[field])
    await user_profile.save()

    # 检查个人信息是否完整
    await check_profile_completed(user_profile)

    return user_profile


@router.post("/bind/identity", summary="实名认证")
async def bind_identity(request: VerifyIdentityRequest, user: UserAuth = Depends(get_current_user)):
    """
    实名认证逻辑
    :param request:
    :param user:
    :return:
    """
    # 验证用户是否存在
    user_profile = await UserProfile.get_or_none(user=user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 检查是否已完成实名认证
    if user_profile.id_card_number:
        raise HTTPException(status_code=400, detail="用户已完成实名认证")

    # 验证身份证号码格式
    if not is_valid_id_card(request.id_card_number):
        raise HTTPException(status_code=400, detail="身份证号码格式错误")

    # todo: 调用第三方实名认证服务验证
    # identity_verified = await verify_identity_with_third_party(request.full_name, request.id_card_number)
    # if not identity_verified:
    #     raise HTTPException(status_code=400, detail="实名认证失败，姓名与身份证号码不匹配")

    # todo: 验证身份证照片内容（OCR 检测）
    # front_verified = await verify_id_card_photo(front_photo_path, "front", full_name, id_card_number)
    # back_verified = await verify_id_card_photo(back_photo_path, "back", full_name, id_card_number)
    # if not (front_verified and back_verified):
    #     raise HTTPException(status_code=400, detail="身份证照片验证失败")

    user_profile.full_name = request.full_name
    user_profile.id_card_number = request.id_card_number
    user_profile.id_card_expiry = request.id_card_expiry
    await user_profile.save()

    # 检查个人信息是否完整
    await check_profile_completed(user_profile)

    return {
        "success": True,
        "msg": "实名认证成功"
    }


@router.post("/bind/academic", summary="学信网认证")
async def bind_academic(request: VerifyAcademicRequest, user: UserAuth = Depends(get_current_user)):
    """
    学信网认证逻辑
    :param request:
    :param user:
    :return:
    """
    # 验证用户是否存在
    user_profile = await UserProfile.get_or_none(user=user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 检查是否已完成学信网认证
    if user_profile.academic_verified:
        raise HTTPException(status_code=400, detail="用户已完成学信网认证")

    # 检查是否已完成实名认证
    if not user_profile.id_card_number:
        raise HTTPException(status_code=400, detail="请先完成实名认证")

    # 验证身份证号码格式
    if not is_valid_id_card(request.id_card_number):
        raise HTTPException(status_code=400, detail="身份证号码格式错误")

    # 检查实名认证信息是否匹配
    if request.full_name != user_profile.full_name or request.id_card_number != user_profile.id_card_number:
        raise HTTPException(status_code=400, detail="实名认证信息不匹配")

    # todo: 验证学信网认证信息
    # 保存用户上传的学信网认证报告
    # academic_report_path = await save_uploaded_file(request.academic_report, "academic", user.id)

    # 模拟调用学信网认证接口验证信息
    # student_verified = await verify_academic_info(request.full_name, request.id_card_number,
    #                                                request.school, request.student_id)
    # if not student_verified:
    #     raise HTTPException(status_code=400, detail="学信网认证失败，信息不匹配")

    # 验证学信网认证报告内容（通过 OCR 或其他方式）
    # report_verified = await verify_academic_report(academic_report_path, full_name,
    #                                                id_card_number, school, student_id)
    # if not report_verified:
    #     raise HTTPException(status_code=400, detail="学信网认证报告验证失败")

    user_profile.academic_verified = True
    await user_profile.save()

    # 检查个人信息是否完整
    await check_profile_completed(user_profile)

    return {
        "success": True,
        "msg": "学信网认证成功"
    }


@router.post("/bind/bank-account", summary="绑定银行卡")
async def bind_bankcard(request: BindBankAccountRequest, user: UserAuth = Depends(get_current_user)):
    """
    银行卡绑定逻辑
    :param request:
    :param user:
    :return:
    """
    # 验证用户是否存在
    user_profile = await UserProfile.get_or_none(user=user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 检查用户是否已完成实名认证
    if not user_profile.id_card_number:
        raise HTTPException(status_code=400, detail="请先完成实名认证")

    # 验证银行卡号格式
    if not request.bank_account.isdigit() or len(request.bank_account) < 12:
        raise HTTPException(status_code=400, detail="银行卡号格式错误")

    # 验证手机号格式
    if not request.phone_number.isdigit() or len(request.phone_number) != 11:
        raise HTTPException(status_code=400, detail="手机号格式错误")

    # todo: 第三方验证银行卡号和手机号是否匹配
    # is_matched = await verify_bank_account(request.bank_account, request.phone_number)

    # if not is_matched:
    #     raise HTTPException(status_code=400, detail="银行卡号和手机号不匹配")

    # 验证验证码
    # is_verified = verify_sms_code(request.verification_code, request.phone_number)

    # if not is_verified:
    #     raise HTTPException(status_code=400, detail="验证码错误或已过期")

    user_profile.bank_account = request.bank_account
    await user_profile.save()

    return {
        "success": True,
        "msg": "银行卡绑定成功"
    }

# @router.post("/bind/phone", summary="换绑手机号")
# async def bind_phone():
#     # 手机号换绑逻辑
#     # todo: bind_phone 手机号换绑逻辑
#     pass


# 检查个人信息是否完善
async def check_profile_completed(user_profile: UserProfile):
    completed = 1
    if not user_profile.full_name:
        completed = 0
    if not user_profile.phone_number:
        completed = 0
    if not user_profile.id_card_number or not user_profile.id_card_expiry:
        completed = 0
    if not user_profile.bank_account:
        completed = 0
    if not user_profile.date_of_birth:
        completed = 0

    if completed:
        user_profile.is_profile_completed = True
    else:
        user_profile.is_profile_completed = False
    await user_profile.save()


