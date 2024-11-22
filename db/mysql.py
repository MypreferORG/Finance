
# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:22 PM
# @Author : Myprefer
# @Des: MySQL数据库连接
"""

from os import getenv
from dotenv import load_dotenv
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


# 加载 .env 文件
load_dotenv()

# MySQL 连接字典
DB_ORM_CONFIG = {
    "connections": {
        "finance": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': getenv("MYSQL_HOST"),
                'user': getenv("MYSQL_USER"),
                'password': getenv("MYSQL_PASSWORD"),
                'port': int(getenv("MYSQL_PORT")),
                'database': getenv("MYSQL_DB"),
            }
        },
        # # "finance": {
        #     'engine': 'tortoise.backends.asyncpg',
        #     "credentials": {
        #         'host': getenv("POSTGRES_HOST"),
        #         'user': getenv("POSTGRES_USER"),
        #         'password': getenv("POSTGRES_PASSWORD"),
        #         'port': int(getenv("POSTGRES_PORT")),
        #         'database': getenv("POSTGRES_DB"),
        #     }
        # },
        # "finance": {
        #     'engine': 'tortoise.backends.odbc',
        #     "credentials": {
        #         'dsn': getenv("ORACLE_DSN"),
        #         'user': getenv("ORACLE_USER"),
        #         'password': getenv("ORACLE_PASSWORD"),
        #     }
        # },
        # "finance": {
        #     'engine': 'tortoise.backends.sqlite',
        #     'credentials': {
        #         'file_path': '/root/Databases/finance/finance.db',  # SQLite 数据库文件路径
        #     }
        # },
    },
    "apps": {
        "finance": {"models": ["models.user", "models.loan", "models.article", "models.notification"], "default_connection": "finance"},
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    """
    注册数据库
    :param app:
    :return:
    """
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )
