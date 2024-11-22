
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


async def register_mysql(app: FastAPI, database: str = 'mysql'):
    """
    注册数据库
    :param app:
    :return:
    """
    database_connection = {}
    if database == 'mysql':
        database_connection = {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': getenv("MYSQL_HOST"),
                'user': getenv("MYSQL_USER"),
                'password': getenv("MYSQL_PASSWORD"),
                'port': int(getenv("MYSQL_PORT")),
                'database': getenv("MYSQL_DB"),
            }
        }
    elif database == 'postgres':
        database_connection = {
            'engine': 'tortoise.backends.asyncpg',
            "credentials": {
                'host': getenv("POSTGRES_HOST"),
                'user': getenv("POSTGRES_USER"),
                'password': getenv("POSTGRES_PASSWORD"),
                'port': int(getenv("POSTGRES_PORT")),
                'database': getenv("POSTGRES_DB"),
            }
        }
    elif database == 'oracle':
        database_connection = {
            'engine': 'tortoise.backends.odbc',
            "credentials": {
                'dsn': getenv("ORACLE_DSN"),
                'user': getenv("ORACLE_USER"),
                'password': getenv("ORACLE_PASSWORD"),
            }
        }
    elif database == 'sqlite':
        database_connection = {
            'engine': 'tortoise.backends.sqlite',
            'credentials': {
                'file_path': 'D:\\ML\\finance\\sqlite-tools-win-x64-3460100\\finance.db',  # SQLite 数据库文件路径
            }
        }
    # MySQL 连接字典
    DB_ORM_CONFIG = {
        "connections": {
            "finance": database_connection,
        },
        "apps": {
            "finance": {"models": ["models.user", "models.loan", "models.article", "models.notification"],
                        "default_connection": "finance"},
        },
        'use_tz': False,
        'timezone': 'Asia/Shanghai'
    }

    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=True,
    )
