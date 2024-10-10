# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:37 PM
# @Author : Myprefer
# @Des: 基本配置文件
"""

from typing import List
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv, find_dotenv


class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)

    # 项目信息
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "finance"
    DESCRIPTION: str = '<a href="/redoc" target="_blank">redoc</a>'

    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]

    # Session
    SECRET_KEY = "session"
    SESSION_COOKIE = "session_id"
    SESSION_MAX_AGE = 7 * 24 * 60 * 60

    # Jwt
    JWT_SECRET_KEY = "89spfhbowh8p3rho0913hnoda132d543sd146988hubh9u887y89829uikprewe32rwerwer"
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

    # 二维码过期时间
    QRCODE_EXPIRE = 60 * 1

    
settings = Config()




