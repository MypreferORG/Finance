# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:22 PM
# @Author : Myprefer
# @Des: Redis连接管理
"""

import aioredis
import os
from aioredis import Redis
from dotenv import load_dotenv

load_dotenv()

CACHE_HOST = os.getenv("CACHE_HOST", '127.0.0.1')
CACHE_PORT = os.getenv("CACHE_PORT", '6379')
CACHE_DB = os.getenv('CACHE_DB', 0)


async def sys_cache() -> Redis:
    """
    系统缓存
    :return: cache 连接池
    """
    # 从URL方式创建redis连接池
    sys_cache_pool = aioredis.ConnectionPool.from_url(
        f"redis://{CACHE_HOST}:{CACHE_PORT}",
        db=CACHE_DB,
        encoding='utf-8',
        decode_responses=True
    )
    return Redis(connection_pool=sys_cache_pool)
