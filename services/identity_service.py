# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/24 22:03
# @Author : Myprefer
# @Des: 
"""

import re

from fastapi import UploadFile, HTTPException
import aiohttp
from config import settings


def is_valid_id_card(id_card_number: str) -> bool:
    """
    验证身份证号码格式（支持中国大陆二代身份证）
    :param id_card_number: 身份证号码
    :return: 是否有效
    """
    id_card_pattern = r"^[0-9]{17}[0-9xX]$"
    return re.match(id_card_pattern, id_card_number) is not None


# 调用 OCR 微服务
async def verify_id_card_photo(file: UploadFile, side: str,
                               full_name: str, id_card_number: str):
    """
    调用 OCR 微服务验证身份证照片内容。
    :param id_card_number:
    :param full_name:
    :param file: 上传的身份证照片
    :param side: "front" 表示正面，"back" 表示反面
    :return: OCR 返回的解析结果
    """
    service_url = settings.OCR_URL  # 你的 OCR 微服务地址
    try:
        # 创建一个 FormData 对象并添加文件
        form_data = aiohttp.FormData()
        form_data.add_field(
            "pic",  # 该字段名需要与服务端的字段名一致
            await file.read(),  # 读取文件内容
            filename=file.filename,
            content_type=file.content_type,
        )
        # form_data.add_field("side", side)  # 添加额外的字段（如身份证正反面）

        # 发送异步请求
        async with aiohttp.ClientSession() as session:
            async with session.post(service_url, data=form_data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="OCR 微服务调用失败")
                result = await response.json()  # 解析 JSON 响应
                # 验证身份证号码和姓名是否匹配
                if result.get("idnum") != id_card_number or result.get("name") != full_name:
                    raise HTTPException(status_code=400, detail="身份证信息不匹配")
                return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 服务错误: {str(e)}")