# -*- coding: utf-8 -*-
"""
# @Create on : 2025/1/16 23:18
# @Author : Myprefer
# @Des: 保存数据相关的工具函数
"""
import os.path
import shutil
from pathlib import Path
from fastapi import UploadFile


async def save_idcard_photo(file: UploadFile, file_type: str, user_id: int) -> str:
    """
    保存用户上传的身份证照片
    :param file: 用户上传的文件
    :param file_type: 文件类型 (front/back)
    :param user_id: 用户ID
    :return: 保存文件的路径
    """
    # 确保目录存在
    UPLOAD_DIR = Path(os.path.join("uploads", "idcard"))
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 构建文件路径
    file_path = UPLOAD_DIR / f"{user_id}_{file_type}.jpg"

    # 保存文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)