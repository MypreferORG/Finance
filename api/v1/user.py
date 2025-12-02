# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 个人信息管理相关接口
"""
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import requests
import uuid
import logging

from api.v1.article import recommend_articles
from models import UserAuth, UserProfile
from models.user import UserApplication, UserBehavior
from models.user_device_data import (
    UserSmsRecord, UserAppRecord, UserContactRecord, 
    UserImageRecord, UserDeviceDataBatch
)
from schemas import UserProfileResponse, UpdateProfileRequest, VerifyIdentityRequest, VerifyAcademicRequest
from schemas.device_data import DeviceDataRequest, DeviceDataResponse
from core.dependences import user_required
from schemas.user import BindBankAccountRequest
from services.identity_service import is_valid_id_card, verify_id_card_photo, verify_identity_with_third_party

from utils.model2dict import model_to_raw_dict
from utils.save import save_idcard_photo
import asyncio

router = APIRouter()
logger = logging.getLogger(__name__)


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

    credit_score = await get_credit_score(user=user)

    # 更新信用分
    user_profile.credit = credit_score.get("credit_score")
    await user_profile.save()
    print(f"用户信用分：{credit_score}")

    # 调用推荐文章逻辑
    # asyncio.create_task(recommend_articles(user=user))

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
    # print(f"身份证号码：{id_card_number}")
    # if not is_valid_id_card(id_card_number):
    #     raise HTTPException(status_code=402, detail="身份证号码格式错误")

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

    # 调用推荐文章逻辑
    # await recommend_articles(user=user)

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

    # 调用推荐文章逻辑
    await recommend_articles(user=user)

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


@router.get("/credit", summary="获取信用分")
async def get_credit_score(user: UserAuth = Depends(user_required)):
    """
    获取用户信用分逻辑
    :param user: UserAuth
    :return:
    """
    # 查询用户信用分
    user_profile = await UserProfile.get_or_none(user=user)
    user_application = await UserApplication.get_or_none(user=user)
    user_behavior = await UserBehavior.get_or_none(user=user)
    if not user_profile or not user_application or not user_behavior:
        raise HTTPException(status_code=404, detail="用户未找到")
    key2remove = ['user']
    user_info = {}
    user_info.update(model_to_raw_dict(user_application, key2remove))
    user_info.update(model_to_raw_dict(user_behavior, key2remove))

    info_str = ''
    for key, value in user_info.items():
        if value is None:
            info_str += ","
        else:
            info_str += str(value) + ","
    info_str = info_str[:-1]  # 去掉最后一个逗号
    print(f"用户信息：{info_str}")
    # 使用requests库发送用户信息到外部API
    
    try:
        response = requests.get(f'http://127.0.0.1:8001/predict/{info_str}', timeout=10)
        response.raise_for_status()  # 检查HTTP错误
        
        credit_data = response.json()
        predictions_a = credit_data.get("predictions_a", [])
        predictions_b = credit_data.get("predictions_b", [])
        # 处理预测结果
        prob_a = predictions_a[0][0] if predictions_a else 0.5
        prob_b = predictions_b[0][0] if predictions_b else 0.5

        result = predictions_a[0][1] and predictions_b[0][1]

        # 计算信用分（假设范围在300到850之间）
        credit_score = int((prob_a + prob_b) / 2 * 850)  # 示例计算公式
        # credit_score = int(prob_a * 850)  # 示例计算公式
        # credit_score = int(prob_b * 850)  # 示例计算公式

        # credit_score = credit_data.get("credit_score", 650)  # 默认值为650
        
        # 更新用户信用分数据
        user_profile.credit_score = credit_score
        await user_profile.save()
        
        return {
            "credit_score": credit_score,
            "result": result,
            "updated_at": user_profile.updated_at,
        }
    except requests.RequestException as e:
        # 记录错误，返回默认或缓存的信用分
        print(f"信用分API请求错误: {str(e)}")
        return {
            "credit_score": user_profile.credit or 200,
            "error": "无法连接到信用评分服务"
        }


@router.post("/device_data", summary="上传设备数据", response_model=DeviceDataResponse)
async def upload_device_data(
    request: DeviceDataRequest,
    user: UserAuth = Depends(user_required)
):
    """
    上传用户设备数据接口
    
    客户端上传短信、应用列表、通讯录、图片等数据，存储到数据库中
    
    Args:
        request: 包含短信、应用、通讯录、图片列表和设备信息的请求体
        user: 当前认证用户
        
    Returns:
        上传结果，包括批次ID和各类数据数量
    """
    # 去重逻辑说明:
    # - SMS: 去重依据 (user, telphone, content, send_date)
    # - App: 优先依据 pkg_name, 否则依据 name。若已存在则尝试更新版本/时间等信息
    # - Contact: 去重依据 (user, phone_number)，若 display_name 不同则更新
    # - Image: 优先依据 image_url 去重，其次依据 (file_name, file_size)。若元信息不同则更新
    try:
        # 生成批次ID
        batch_id = f"batch_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}"
        logger.info(f"用户 {user.id} 开始上传设备数据，批次ID: {batch_id}")
        
        # 统计各类数据
        sms_count = 0
        app_count = 0
        contact_count = 0
        image_count = 0
        # 去重/更新计数
        sms_skipped = 0
        app_skipped = 0
        app_updated = 0
        contact_skipped = 0
        contact_updated = 0
        image_skipped = 0
        
        # 确定数据类型
        data_types = []
        if request.sms_list:
            data_types.append("sms")
        if request.app_list:
            data_types.append("app")
        if request.contact_list:
            data_types.append("contact")
        if request.image_list:
            data_types.append("image")
        data_type = ",".join(data_types) if data_types else "empty"
        
        total_count = (
            len(request.sms_list or []) + 
            len(request.app_list or []) + 
            len(request.contact_list or []) + 
            len(request.image_list or [])
        )
        
        # 创建批次记录
        batch_record = await UserDeviceDataBatch.create(
            user=user,
            batch_id=batch_id,
            data_type=data_type,
            total_count=total_count,
            status="processing"
        )
        
        # 保存短信数据
        if request.sms_list:
            for sms in request.sms_list:
                try:
                    send_date = None
                    if sms.sendDate:
                        try:
                            send_date = datetime.strptime(sms.sendDate, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
                    
                    sms_type = "received" if sms.type == "1" else "sent"
                    # 检查是否已存在（user+telphone+content+send_date）
                    content_norm = sms.content.strip() if isinstance(sms.content, str) else sms.content
                    telphone_norm = sms.telphone.strip() if isinstance(sms.telphone, str) else sms.telphone
                    filter_kwargs = {"user": user, "telphone": telphone_norm, "content": content_norm}
                    if send_date:
                        filter_kwargs["send_date"] = send_date
                    # 注意: get_or_none 会抛出 MultipleObjectsReturned，如果 DB 有重复记录。
                    # 使用 filter().first() 避免抛异常，并记录是否存在多个重复项以便清理。
                    existing_sms_count = await UserSmsRecord.filter(**filter_kwargs).count()
                    if existing_sms_count > 1:
                        logger.warning(f"用户 {user.id} 存在多条相同短信记录，filter={filter_kwargs}, count={existing_sms_count}")
                    existing_sms = await UserSmsRecord.filter(**filter_kwargs).first()
                    if existing_sms:
                        sms_skipped += 1
                    else:
                        await UserSmsRecord.create(
                            user=user,
                            telphone=telphone_norm,
                            content=content_norm,
                            send_date=send_date,
                            sms_type=sms_type
                        )
                        sms_count += 1
                except Exception as e:
                    logger.warning(f"保存短信失败: {e}")
        
        # 保存应用列表数据
        if request.app_list:
            for app in request.app_list:
                try:
                    install_time = None
                    last_update_time = None
                    if app.install_time:
                        try:
                            install_time = datetime.strptime(app.install_time, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
                    if app.last_update_time:
                        try:
                            last_update_time = datetime.strptime(app.last_update_time, "%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
                    
                    # 去重：优先使用 pkg_name, 否则使用 name
                    pkg_name_norm = app.pkg_name.strip() if isinstance(app.pkg_name, str) else app.pkg_name
                    name_norm = app.name.strip() if isinstance(app.name, str) else app.name
                    if pkg_name_norm:
                        existing_app_count = await UserAppRecord.filter(user=user, pkg_name=pkg_name_norm).count()
                        if existing_app_count > 1:
                            logger.warning(f"用户 {user.id} 存在多条相同应用记录 pkg_name={pkg_name_norm}, count={existing_app_count}")
                        existing_app = await UserAppRecord.filter(user=user, pkg_name=pkg_name_norm).first()
                    else:
                        existing_app_count = await UserAppRecord.filter(user=user, name=name_norm).count()
                        if existing_app_count > 1:
                            logger.warning(f"用户 {user.id} 存在多条相同应用记录 name={name_norm}, count={existing_app_count}")
                        existing_app = await UserAppRecord.filter(user=user, name=name_norm).first()

                    if existing_app:
                        # 更新字段（优先写入非空值）
                        updated = False
                        if app.version_name and app.version_name != existing_app.version_name:
                            existing_app.version_name = app.version_name
                            updated = True
                        if app.version_code and app.version_code != existing_app.version_code:
                            existing_app.version_code = app.version_code
                            updated = True
                        if app.is_system_app is not None and app.is_system_app != existing_app.is_system_app:
                            existing_app.is_system_app = app.is_system_app
                            updated = True
                        if install_time and install_time != existing_app.install_time:
                            existing_app.install_time = install_time
                            updated = True
                        if last_update_time and last_update_time != existing_app.last_update_time:
                            existing_app.last_update_time = last_update_time
                            updated = True
                        if updated:
                            await existing_app.save()
                            app_updated += 1
                        else:
                            app_skipped += 1
                    else:
                        await UserAppRecord.create(
                            user=user,
                            name=name_norm,
                            pkg_name=pkg_name_norm,
                            version_name=app.version_name,
                            version_code=app.version_code,
                            is_system_app=app.is_system_app or False,
                            install_time=install_time,
                            last_update_time=last_update_time
                        )
                        app_count += 1
                except Exception as e:
                    logger.warning(f"保存应用记录失败: {e}")
        
        # 保存通讯录数据
        if request.contact_list:
            for contact in request.contact_list:
                try:
                    phone_norm = contact.phone_number.strip() if isinstance(contact.phone_number, str) else contact.phone_number
                    existing_contact_count = await UserContactRecord.filter(user=user, phone_number=phone_norm).count()
                    if existing_contact_count > 1:
                        logger.warning(f"用户 {user.id} 存在多条相同联系人记录 phone={phone_norm}, count={existing_contact_count}")
                    existing_contact = await UserContactRecord.filter(user=user, phone_number=phone_norm).first()
                    if existing_contact:
                        # 如果 display_name 有变更则更新
                        if contact.display_name and contact.display_name != existing_contact.display_name:
                            existing_contact.display_name = contact.display_name
                            await existing_contact.save()
                            contact_updated += 1
                        else:
                            contact_skipped += 1
                    else:
                        await UserContactRecord.create(
                            user=user,
                            display_name=contact.display_name,
                            phone_number=phone_norm,
                            phone_number_raw=contact.phone_number_raw,
                            phone_type=contact.phone_type
                        )
                        contact_count += 1
                except Exception as e:
                    logger.warning(f"保存联系人失败: {e}")
        
        # 保存图片数据
        if request.image_list:
            for image in request.image_list:
                try:
                    # 支持新的图片字段: path,name,size,type
                    image_type = getattr(image, 'image_type', None) or None
                    # 优先使用 path 作为 image_url 的存储值
                    image_url = getattr(image, 'path', None) or getattr(image, 'image_url', None)
                    file_name = getattr(image, 'name', None)
                    if isinstance(file_name, str):
                        file_name = file_name.strip()
                    file_size = getattr(image, 'size', None)
                    mime_type = getattr(image, 'mime_type', None) or getattr(image, 'type', None)

                    # 去重：优先使用 image_url 去重，其次使用 file_name + file_size
                    existing_image = None
                    if image_url:
                        existing_image_count = await UserImageRecord.filter(user=user, image_url=image_url).count()
                        if existing_image_count > 1:
                            logger.warning(f"用户 {user.id} 存在多条相同图片记录 image_url={image_url}, count={existing_image_count}")
                        existing_image = await UserImageRecord.filter(user=user, image_url=image_url).first()
                    elif file_name and file_size:
                        existing_image_count = await UserImageRecord.filter(user=user, file_name=file_name, file_size=file_size).count()
                        if existing_image_count > 1:
                            logger.warning(f"用户 {user.id} 存在多条相同图片记录 file_name={file_name}, file_size={file_size}, count={existing_image_count}")
                        existing_image = await UserImageRecord.filter(user=user, file_name=file_name, file_size=file_size).first()

                    if existing_image:
                        # 如果元信息有变化则更新
                        updated = False
                        if image_type and image_type != existing_image.image_type:
                            existing_image.image_type = image_type
                            updated = True
                        if mime_type and mime_type != existing_image.mime_type:
                            existing_image.mime_type = mime_type
                            updated = True
                        if file_name and file_name != existing_image.file_name:
                            existing_image.file_name = file_name
                            updated = True
                        if file_size and file_size != existing_image.file_size:
                            existing_image.file_size = file_size
                            updated = True
                        new_image_data = getattr(image, 'image_data', None)
                        if new_image_data and new_image_data != existing_image.image_data:
                            existing_image.image_data = new_image_data
                            updated = True
                        if updated:
                            await existing_image.save()
                            image_count += 1
                        else:
                            image_skipped += 1
                    else:
                        await UserImageRecord.create(
                            user=user,
                            image_type=image_type,
                            image_url=image_url,
                            file_name=file_name,
                            file_size=file_size,
                            mime_type=mime_type,
                            image_data=getattr(image, 'image_data', None)
                        )
                        image_count += 1
                except Exception as e:
                    logger.warning(f"保存图片记录失败: {e}")
        
        # 更新批次记录
        success_count = sms_count + app_count + app_updated + contact_count + contact_updated + image_count
        duplicates_skipped_total = sms_skipped + app_skipped + contact_skipped + image_skipped
        failed_count = total_count - success_count - duplicates_skipped_total
        if failed_count < 0:
            failed_count = 0

        batch_record.success_count = success_count
        batch_record.failed_count = failed_count
        batch_record.status = "completed"
        await batch_record.save()

        logger.info(f"用户 {user.id} 设备数据上传完成，成功: {success_count}, 失败: {failed_count}, 去重跳过: {duplicates_skipped_total}")

        return DeviceDataResponse(
            code=200,
            message="数据上传成功",
            data={
                "batch_id": batch_id,
                "sms_count": sms_count,
                "sms_skipped": sms_skipped,
                "app_count": app_count,
                "app_updated": app_updated,
                "app_skipped": app_skipped,
                "contact_count": contact_count,
                "contact_updated": contact_updated,
                "contact_skipped": contact_skipped,
                "image_count": image_count,
                "image_skipped": image_skipped,
                "duplicates_skipped": duplicates_skipped_total,
                "total_success": success_count,
                "total_failed": failed_count
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"设备数据上传失败: {str(e)}", exc_info=True)
        # 更新批次状态为失败
        if 'batch_record' in locals():
            batch_record.status = "failed"
            batch_record.error_message = str(e)
            await batch_record.save()
        raise HTTPException(status_code=500, detail=f"数据上传失败: {str(e)}")
