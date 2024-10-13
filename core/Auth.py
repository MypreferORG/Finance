# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:33 PM
# @Author : Myprefer
# @Des: JWT鉴权
"""
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from config import settings
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# 配置密码加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# JWT payload模型
class TokenData(BaseModel):
    username: str
    roles: list


# 用于创建JWT的函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 加密密码
def get_password_hash(password):
    return pwd_context.hash(password)


# 验证JWT token
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


