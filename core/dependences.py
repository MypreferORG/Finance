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
