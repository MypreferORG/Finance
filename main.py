# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:24 PM
# @Author : Myprefer
# @Des: FastAPI 主入口文件
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.Events import startup, stopping
from api.v1.base import user_api_router
from api.v2.base import admin_api_router
from config import settings


app = FastAPI()

# 事件监听
app.add_event_handler("startup", startup(app))
app.add_event_handler("shutdown", stopping(app))

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 注册API路由
app.include_router(user_api_router)
app.include_router(admin_api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.FASTAPI_PORT)
