# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/18 21:55
# @Author : Jason
# @Des: 用户管理接口
"""
from fastapi import APIRouter, HTTPException, Query
from models.user import UserAuth, UserSignLog, UserProfile
from schemas.v2.user import UserProfileResponse, UserSignLogFilterRequest, UserSignLogResponse, UserAuthResponse, \
    UserAuthFilterRequest, UpdateUserAuthRequest, UpdateUserProfileRequest, CreateUserAuthRequest, \
    CreateUserProfileRequest
from typing import List, Optional
from pydantic import BaseModel
router = APIRouter()

@router.post("/auth", summary="新增用户认证信息")
async def create_user_auth(request: CreateUserAuthRequest):
    """
    新增用户认证信息
    :param request: 新用户的信息
    :return: 创建结果
    """
    # 检查用户名是否唯一
    existing_user = await UserAuth.get_or_none(username=request.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查手机号是否唯一
    existing_phone = await UserAuth.get_or_none(phone_number=request.phone_number)
    if existing_phone:
        raise HTTPException(status_code=400, detail="手机号已存在")

    # 创建新用户
    new_user = await UserAuth.create(
        username=request.username,
        phone_number=request.phone_number,
        hashed_password=request.password,  # 直接存储明文密码
        role=request.role,
    )

    return {"msg": "用户认证信息创建成功", "user_id": new_user.id}

@router.get("/auth", summary="获取用户认证信息列表", response_model=List[UserAuthResponse])
async def get_user_auth(
        username: str = Query(None, description="按用户名筛选"),
        phone_number: str = Query(None, description="按手机号筛选"),
        role: str = Query(None, description="按角色筛选 (user/admin/root)"),
        page: int = Query(1, description="分页页码"),
        limit: int = Query(10, description="分页大小"),
):
    """
    获取所有用户的认证信息，支持筛选和分页
    """
    query = UserAuth.all()

    # 添加筛选条件
    if username:
        query = query.filter(username__icontains=username)
    if phone_number:
        query = query.filter(phone_number__icontains=phone_number)
    if role:
        query = query.filter(role=role)

    # 分页
    total = await query.count()
    users = await query.offset((page - 1) * limit).limit(limit)

    if not users:
        raise HTTPException(status_code=404, detail="没有找到符合条件的用户信息")

    return users

@router.get("/auth/{user_id}", summary="获取单个用户认证信息", response_model=UserAuthResponse)
async def get_user_auth_by_id(user_id: str):
    """
    根据用户ID获取用户的认证信息
    :param user_id: 用户ID
    :return: 用户认证信息
    """
    user = await UserAuth.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user

@router.put("/auth/{user_id}", summary="修改用户认证信息")
async def update_user_auth(user_id: str, request: UpdateUserAuthRequest):
    """
    修改用户认证信息
    :param user_id: 用户ID
    :param request: 要修改的字段
    :return: 修改结果
    """
    # 获取用户
    user = await UserAuth.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 更新字段
    if request.username:
        # 检查用户名是否唯一
        existing_user = await UserAuth.get_or_none(username=request.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=400, detail="用户名已存在")
        user.username = request.username

    if request.phone_number:
        # 检查手机号是否唯一
        existing_phone = await UserAuth.get_or_none(phone_number=request.phone_number)
        if existing_phone and existing_phone.id != user_id:
            raise HTTPException(status_code=400, detail="手机号已存在")
        user.phone_number = request.phone_number

    if request.role:
        if request.role not in ["user", "admin", "root"]:
            raise HTTPException(status_code=400, detail="无效的角色类型")
        user.role = request.role

    # 保存修改
    await user.save()

    return {"msg": "用户认证信息修改成功", "user_id": user_id}

@router.post("/profiles", summary="新增用户个人信息")
async def create_user_profile(request: CreateUserProfileRequest):
    """
    新增用户个人信息
    :param request: 新用户个人信息
    :return: 创建结果
    """
    # 检查用户是否存在
    user = await UserAuth.get_or_none(id=request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 检查是否已存在个人信息
    existing_profile = await UserProfile.get_or_none(user=user)
    if existing_profile:
        raise HTTPException(status_code=400, detail="该用户的个人信息已存在")

    # 创建新个人信息
    new_profile = await UserProfile.create(
        user=user,
        full_name=request.full_name,
        phone_number=request.phone_number or user.phone_number,
        gender=request.gender,
        address=request.address,
        date_of_birth=request.date_of_birth,
        income=request.income,
    )

    return {"msg": "用户个人信息创建成功", "profile_id": new_profile.id}

@router.delete("/auth/{user_id}", summary="删除用户及关联信息")
async def delete_user_auth(user_id: str):
    """
    删除用户及其关联信息
    :param user_id: 用户ID
    :return: 删除结果
    """
    # 获取用户
    user = await UserAuth.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 删除关联的登录日志
    await UserSignLog.filter(user=user).delete()

    # 删除关联的个人信息
    await UserProfile.filter(user=user).delete()

    # 删除用户本身
    await user.delete()

    return {"msg": "用户及其关联信息删除成功", "user_id": user_id}

@router.get("/logs", summary="获取所有用户登录日志", response_model=List[UserSignLogResponse])
async def get_user_logs(
        user_id: Optional[str] = None,
        page: int = Query(1, description="分页页码"),
        limit: int = Query(10, description="分页大小")
):
    """
    获取所有用户登录日志
    :param user_id: 按用户ID筛选
    :param page: 分页页码
    :param limit: 每页大小
    :return: 登录日志列表
    """
    query = UserSignLog.all()

    # 筛选条件
    if user_id:
        query = query.filter(user__id=user_id)

    # 分页
    total = await query.count()
    logs = await query.offset((page - 1) * limit).limit(limit)

    if not logs:
        raise HTTPException(status_code=404, detail="没有找到符合条件的登录日志")

    return logs

@router.get("/logs/{user_id}", summary="获取指定用户的登录日志", response_model=List[UserSignLogResponse])
async def get_user_logs_by_id(user_id: str):
    """
    获取指定用户的登录日志
    :param user_id: 用户ID
    :return: 登录日志列表
    """
    logs = await UserSignLog.filter(user__id=user_id).order_by("-created_at")

    if not logs:
        raise HTTPException(status_code=404, detail="没有找到该用户的登录日志")

    return logs

@router.delete("/logs/{log_id}", summary="删除指定登录日志")
async def delete_user_log(log_id: int):
    """
    删除指定登录日志
    :param log_id: 日志ID
    :return: 删除结果
    """
    log = await UserSignLog.get_or_none(id=log_id)
    if not log:
        raise HTTPException(status_code=404, detail="登录日志未找到")

    await log.delete()
    return {"msg": "登录日志删除成功", "log_id": log_id}

@router.post("/logs/filter", summary="按条件筛选登录日志", response_model=List[UserSignLogResponse])
async def filter_user_logs(
        filter: UserSignLogFilterRequest,
        page: int = Query(1, description="分页页码"),
        limit: int = Query(10, description="分页大小")
):
    """
    按条件筛选登录日志
    :param filter: 筛选条件
    :param page: 分页页码
    :param limit: 每页大小
    :return: 登录日志列表
    """
    query = UserSignLog.all()

    # 根据筛选条件添加过滤
    if filter.action:
        query = query.filter(action=filter.action)
    if filter.ip_address:
        query = query.filter(ip_address__icontains=filter.ip_address)
    if filter.start_time:
        query = query.filter(created_at__gte=filter.start_time)
    if filter.end_time:
        query = query.filter(created_at__lte=filter.end_time)

    # 分页
    total = await query.count()
    logs = await query.offset((page - 1) * limit).limit(limit)

    if not logs:
        raise HTTPException(status_code=404, detail="没有找到符合条件的登录日志")

    return logs

@router.get("/profiles", summary="获取所有用户的个人信息", response_model=List[UserProfileResponse])
async def get_all_user_profiles(
        page: int = Query(1, description="分页页码"),
        limit: int = Query(10, description="分页大小")
):
    """
    获取所有用户的个人信息
    :param page: 分页页码
    :param limit: 每页大小
    :return: 用户个人信息列表
    """
    query = UserProfile.all()

    # 分页
    total = await query.count()
    profiles = await query.offset((page - 1) * limit).limit(limit)

    if not profiles:
        raise HTTPException(status_code=404, detail="没有找到用户个人信息")

    return profiles

@router.get("/profiles/{user_id}", summary="获取指定用户的个人信息", response_model=UserProfileResponse)
async def get_user_profile_by_id(user_id: str):
    """
    获取指定用户的个人信息
    :param user_id: 用户ID
    :return: 用户个人信息
    """
    profile = await UserProfile.get_or_none(user__id=user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="用户个人信息未找到")

    return profile

@router.put("/profiles/{user_id}", summary="修改用户个人信息")
async def update_user_profile(user_id: str, request: UpdateUserProfileRequest):
    """
    修改用户个人信息
    :param user_id: 用户ID
    :param request: 修改内容
    :return: 修改结果
    """
    profile = await UserProfile.get_or_none(user__id=user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="用户个人信息未找到")

    # 更新字段
    for field, value in request.dict(exclude_unset=True).items():
        setattr(profile, field, value)

    await profile.save()

    return {"msg": "用户个人信息修改成功", "user_id": user_id}

@router.put("/profiles/{user_id}/complete", summary="标记用户为已完善个人信息")
async def mark_profile_as_completed(user_id: str):
    """
    标记用户为已完善个人信息
    :param user_id: 用户ID
    :return: 操作结果
    """
    profile = await UserProfile.get_or_none(user__id=user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="用户个人信息未找到")

    profile.is_profile_completed = True
    await profile.save()

    return {"msg": "用户个人信息已标记为完善", "user_id": user_id}

@router.delete("/profiles/{user_id}", summary="删除用户个人信息")
async def delete_user_profile(user_id: str, keep_auth: bool = Query(False, description="是否保留用户认证信息")):
    """
    删除用户个人信息
    :param user_id: 用户ID
    :param keep_auth: 是否保留用户认证信息
    :return: 删除结果
    """
    profile = await UserProfile.get_or_none(user__id=user_id)

    if not profile:
        raise HTTPException(status_code=404, detail="用户个人信息未找到")

    # 删除个人信息
    await profile.delete()

    if not keep_auth:
        # 删除用户认证信息及登录日志
        user = await UserAuth.get_or_none(id=user_id)
        if user:
            await UserSignLog.filter(user=user).delete()
            await user.delete()

    return {"msg": "用户个人信息删除成功", "user_id": user_id, "keep_auth": keep_auth}

