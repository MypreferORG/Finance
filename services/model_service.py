# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/26
# @Author : Myprefer
# @Des: 模型上传服务
"""

import os
import shutil
from fastapi import UploadFile, HTTPException
from models.model import AIModel
from datetime import datetime
import uuid


# 有效的模型文件扩展名
ALLOWED_EXTENSIONS = {'.pth', '.ckpt', '.pkl', '.h5', '.pb', '.onnx', '.joblib'}
# 最大文件大小限制（500MB，单位：字节）
MAX_FILE_SIZE = 5000 * 1024 * 1024


def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lower()


def validate_model_file(file: UploadFile) -> None:
    """验证模型文件格式和大小"""
    # 检查文件扩展名
    extension = get_file_extension(file.filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式，允许的格式：{', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 检查文件大小
    file_size = 0
    file.file.seek(0, 2)  # 移动到文件末尾
    file_size = file.file.tell()  # 获取当前位置（文件大小）
    file.file.seek(0)  # 重置文件指针到开头
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"文件大小超过限制，最大允许大小: {MAX_FILE_SIZE/(1024*1024)}MB"
        )


async def upload_model_file(
    file: UploadFile,
    name: str,
    version: str,
    description: str,
    technical_details: str = None
) -> dict:
    """
    上传模型文件并保存到数据库
    """
    try:
        # 验证文件
        validate_model_file(file)
        
        # 获取文件大小
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        # 生成唯一文件名
        extension = get_file_extension(file.filename)
        unique_filename = f"{name.replace(' ', '_')}_{version}_{uuid.uuid4().hex}{extension}"

        # 确保ai/model目录存在
        ai_dir = os.path.join(os.getcwd(), "ai", "model")
        if not os.path.exists(ai_dir):
            os.makedirs(ai_dir)
        
        # 构建文件保存路径
        file_path = os.path.join(ai_dir, unique_filename)
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 保存模型信息到数据库
        file_url = f"/ai/model/{unique_filename}"

        # 使用Tortoise ORM创建模型记录
        new_model = await AIModel.create(
            name=name,
            version=version,
            file_path=file_path,
            description=description,
            technical_details=technical_details,
            file_size=file_size,
            file_extension=extension,
        )
        
        # 返回上传结果
        return {
            "id": new_model.id,
            "name": name,
            "version": version,
            "fileUrl": file_url,
            "description": description,
            "technical_details": technical_details,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size": file_size
        }
    
    except Exception as e:
        # 确保在出现异常时文件句柄被关闭
        file.file.close()
        raise HTTPException(status_code=500, detail=f"上传模型文件失败: {str(e)}")