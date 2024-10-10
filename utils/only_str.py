# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/10 23:06
# @Author : Myprefer
# @Des: 唯一随机字符
"""

import hashlib
import uuid


def random_str():
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    return str(only)
