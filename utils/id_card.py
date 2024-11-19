# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/18 19:06
# @Author : Myprefer
# @Des: 验证身份证号码格式
"""
import re


def is_valid_id_card(id_card_number: str) -> bool:
    """
    验证身份证号码格式（支持中国大陆二代身份证）
    :param id_card_number: 身份证号码
    :return: 是否有效
    """
    id_card_pattern = r"^[0-9]{17}[0-9xX]$"
    return re.match(id_card_pattern, id_card_number) is not None
