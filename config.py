# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:37 PM
# @Author : Myprefer
# @Des: 基本配置文件
"""
import os
from typing import List
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv, find_dotenv


class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)
    BASE_DIR = os.path.dirname('.')

    # 项目信息
    VERSION: str = "1.0.0"
    PROJECT_NAME: str = "finance"
    DESCRIPTION: str = '<a href="/redoc" target="_blank">redoc</a>'

    # 数据库配置
    DATABASE = 'mysql'   # mysql, postgres, oracle, sqlite

    OCR_URL = f'http://localhost:5000/'

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
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60 * 10

    JWT_TOKEN_URL = "v1/auth/login"

    # 二维码过期时间
    QRCODE_EXPIRE = 60 * 1

    ALIPAY_APP_ID = os.getenv('ALIPAY_APP_ID'),  # 应用ID(上线之后需要改成，真实应用的appid)
    APLIPAY_APP_NOTIFY_URL = None,  # 应用回调地址[支付成功以后,支付宝返回结果到哪一个地址下面] 一般这里不写，用下面的回调网址即可
    ALIPAY_DEBUG = False,
    # APIPAY_GATEWAY="https://openapi.alipay.com/gateway.do"   # 真实网关
    APIPAY_GATEWAY = "https://openapi.alipaydev.com/gateway.do",  # 沙盒环境的网关(上线需要进行修改)
    ALIPAY_RETURN_URL = "http://127.0.0.1:8000/alipay/result/",  # 同步回调网址--用于前端,支付成功之后回调
    ALIPAY_NOTIFY_URL = "http://127.0.0.1:8000/alipay/result/",  # 异步回调网址---后端使用，post请求，网站未上线，post无法接收到响应内容，付成功之后回调
    APP_PRIVATE_KEY_STRING = os.path.join(BASE_DIR, 'files/应用私钥2048.txt'),  # 自己生成的私钥，这个就是路径拼接，配置好了，试试能不能点进去
    # 支付宝的公钥，验证支付宝回传消息使用
    ALIPAY_PUBLIC_KEY_STRING = os.path.join(BASE_DIR, 'files/alipay_public'),  # 一定要注意，是支付宝给你的公钥，不是你自己生成的那个
    SIGN_TYPE = "RSA2",  # RSA 或者 RSA2  现在基本上都是用RSA2

    #
    RL_SMS_TEMPLATE_ID = os.getenv('RL_SMS_TEMPLATE_ID'),
    RL_TEST_MOBILE = os.getenv('RL_TEST_MOBILE'),



settings = Config()




