# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/11 16:49
# @Author : Myprefer
# @Des: 依赖注入
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import settings
from core.Auth import verify_jwt_token
from db.redis import sys_cache
from models.user import UserAuth

# 定义从请求头中获取JWT Token的方式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.JWT_TOKEN_URL)


# 验证Token并获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    cache = await sys_cache()
    payload = verify_jwt_token(token)

    # 检查JWT是否在Redis中存在
    if not payload or not await cache.exists(f"jwt:{payload['sub']}"):
        raise credentials_exception

    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await UserAuth.get_or_none(id=user_id)
    if user is None:
        raise credentials_exception

    return user


# 验证Token并检查权限
async def check_permissions(token: str = Depends(oauth2_scheme), scope=Depends()):
    current_user = await get_current_user(token)
    if scope:
        scope_levels = {
            "root": 2,
            "admin": 1,
            "user": 0
        }
        scope_level = scope_levels.get(scope)
        user_scope_level = scope_levels.get(current_user.role)
        if user_scope_level < scope_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足",
            )

    return current_user


# 检查用户是否为管理员
async def admin_required(token: str = Depends(oauth2_scheme)):
    return await check_permissions(token, "admin")


# 检查用户是否为超级管理员
async def root_required(token: str = Depends(oauth2_scheme)):
    return await check_permissions(token, "root")


# 检查用户是否为普通用户
async def user_required(token: str = Depends(oauth2_scheme)):
    return await check_permissions(token, "user")
