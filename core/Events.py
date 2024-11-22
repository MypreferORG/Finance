# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:33 PM
# @Author : Myprefer
# @Des: fastapi事件监听
"""

from typing import Callable
from fastapi import FastAPI
from pyfiglet import figlet_format
import config
from db.mysql import register_mysql


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """
    async def app_start() -> None:

        # 注册数据库
        await register_mysql(app, database=config.settings.DATABASE)
        # APP启动完成后触发
        ascii_art = figlet_format("FastAPI", font="slant")
        print(ascii_art)
    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """
    async def stop_app() -> None:
        # APP停止时触发
        print("停止")
    return stop_app
