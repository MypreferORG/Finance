# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 个人信息管理相关接口
"""
from datetime import date
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from models import UserAuth, UserProfile
from schemas import UserProfileResponse, UpdateProfileRequest, VerifyIdentityRequest, VerifyAcademicRequest
from core.dependences import user_required
from schemas.user import BindBankAccountRequest
from services.identity_service import is_valid_id_card, verify_id_card_photo, verify_identity_with_third_party
from tempfile import NamedTemporaryFile

from utils.save import save_idcard_photo

router = APIRouter()


@router.get("/profile", summary="查看个人信息", response_model=UserProfileResponse)
async def get_profile(user: UserAuth = Depends(user_required)):
    """
    查看个人信息逻辑
    :param user: UserAuth
    :return: user_profile: UserProfileResponse
    """
    # 查询用户个人信息
    user_profile = await UserProfile.get_or_none(user=user)

    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user_profile


@router.post("/profile/update", summary="编辑个人信息", response_model=UserProfileResponse)
async def update_profile(request: UpdateProfileRequest, user: UserAuth = Depends(user_required)):
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

    return user_profile


@router.post("/bind/identity", summary="实名认证")
async def bind_identity(
    full_name: str = Form(...),  # 普通表单字段
    id_card_number: str = Form(...),  # 普通表单字段
    id_card_expiry: date = Form(...),  # 可选表单字段
    front_photo: UploadFile = File(...),  # 身份证正面照片
    back_photo: UploadFile = File(...),  # 身份证反面照片
    user: UserAuth = Depends(user_required)
):
    """
    实名认证逻辑
    :param full_name:
    :param id_card_number:
    :param id_card_expiry:
    :param front_photo:
    :param back_photo:
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
    if not is_valid_id_card(id_card_number):
        raise HTTPException(status_code=402, detail="身份证号码格式错误")

    # 检查身份证有效期是否过期
    if id_card_expiry < date.today():
        raise HTTPException(status_code=406, detail="身份证已过期")

    # 保存上传的身份证照片
    front_path = await save_idcard_photo(front_photo, "front", user.id)
    back_path = await save_idcard_photo(back_photo, "back", user.id)

    idcard_details = {
        "name": full_name,
        "idNumber": id_card_number,
        "id_card_expiry": id_card_expiry
    }

    # 调用第三方实名认证服务验证
    # identity_verified = await verify_identity_with_third_party(front_path, back_path, idcard_details)
    identity_verified = True  # 模拟验证通过
    if not identity_verified:
        raise HTTPException(status_code=405, detail="实名认证失败，姓名与身份证号码不匹配")

    # 验证身份证照片内容
    # front_verified = await verify_id_card_photo(front_photo, "front", full_name, id_card_number)
    # back_verified = await verify_id_card_photo(back_photo, "back", )
    # front_verified = True
    # back_verified = True  # 模拟验证通过
    # if not (front_verified and back_verified):
    #     raise HTTPException(status_code=405, detail="身份证照片验证失败")

    user_profile.full_name = full_name
    user_profile.id_card_number = id_card_number
    user_profile.id_card_expiry = id_card_expiry
    await user_profile.save()

    return {
        "success": True,
        "msg": "实名认证成功"
    }


@router.post("/bind/academic", summary="学信网认证")
async def bind_academic(request: VerifyAcademicRequest, user: UserAuth = Depends(user_required)):
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
    if user_profile.student_verified:
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

    user_profile.student_verified = True
    await user_profile.save()

    return {
        "success": True,
        "msg": "学信网认证成功"
    }


@router.post("/bind/bank-account", summary="绑定银行卡")
async def bind_bankcard(request: BindBankAccountRequest, user: UserAuth = Depends(user_required)):
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
