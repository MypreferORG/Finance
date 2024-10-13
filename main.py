# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:24 PM
# @Author : Myprefer
# @Des: FastAPI 主入口文件
"""

from fastapi import FastAPI
from core.Events import startup, stopping
from api.base import api_router
from dotenv import load_dotenv


app = FastAPI(
    
)

# 事件监听
app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", stopping(app))

# 注册API路由
app.include_router(api_router)
