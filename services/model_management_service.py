# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/26
# @Author : Myprefer
# @Des: 模型管理服务
"""

import os
import shutil
from fastapi import UploadFile, HTTPException
from models.model import AIModel
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import uuid
from tortoise.expressions import Q
from tortoise.queryset import QuerySet


# 有效的模型文件扩展名
ALLOWED_EXTENSIONS = {'.pth', '.ckpt', '.pkl', '.h5', '.pb', '.onnx', '.joblib'}
# 最大文件大小限制（500MB，单位：字节）
MAX_FILE_SIZE = 500 * 1024 * 1024


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
            detail={
                "message": "文件格式不支持",
                "supportedFormats": list(ALLOWED_EXTENSIONS)
            }
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
    technical_details: str = None,
    metrics: dict = None
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
        model_data = {
            "name": name,
            "version": version,
            "file_path": file_path,
            "description": description,
            "technical_details": technical_details,
            "file_size": file_size,
            "file_extension": extension,
            "status": "testing"
        }
        
        # 如果提供了metrics，添加到模型数据中
        if metrics:
            model_data.update({
                "ks_value": metrics.get("ksValue"),
                "bad_rate": metrics.get("badRate"),
                "accuracy": metrics.get("accuracy"),
                "recall": metrics.get("recall"),
                "precision": metrics.get("precision")
            })

        # 使用Tortoise ORM创建模型记录
        new_model = await AIModel.create(**model_data)
        
        # 返回上传结果
        return {
            "id": new_model.id,
            "name": name,
            "version": version,
            "status": "testing",
            "fileName": unique_filename,
            "fileSize": file_size,
            "uploadTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "description": description,
            "ksValue": new_model.ks_value,
            "badRate": new_model.bad_rate,
            "accuracy": new_model.accuracy,
            "recall": new_model.recall,
            "precision": new_model.precision
        }
    
    except Exception as e:
        # 确保在出现异常时文件句柄被关闭
        if hasattr(file, 'file'):
            file.file.close()
        raise HTTPException(status_code=500, detail=f"上传模型文件失败: {str(e)}")


async def get_model_list(
    page_no: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """获取模型列表"""
    
    # 构建查询条件
    query = AIModel.all()
    
    if status:
        query = query.filter(status=status)
    
    if name:
        query = query.filter(name__icontains=name)
    
    # 获取总数
    total = await query.count()
    
    # 分页查询
    offset = (page_no - 1) * page_size
    models = await query.offset(offset).limit(page_size).order_by('-created_at')
    
    # 转换为响应格式
    records = []
    for model in models:
        records.append({
            "id": model.id,
            "name": model.name,
            "version": model.version,
            "status": model.status,
            "ksValue": model.ks_value,
            "badRate": model.bad_rate,
            "accuracy": model.accuracy,
            "recall": model.recall,
            "precision": model.precision,
            "createTime": model.created_at.strftime("%Y-%m-%d %H:%M:%S") if model.created_at else None,
            "updateTime": model.updated_at.strftime("%Y-%m-%d %H:%M:%S") if model.updated_at else None,
            "description": model.description
        })
    
    return {
        "records": records,
        "total": total,
        "pageNo": page_no,
        "pageSize": page_size
    }


async def get_model_detail(model_id: int) -> Dict[str, Any]:
    """获取模型详情"""
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    return {
        "id": model.id,
        "name": model.name,
        "version": model.version,
        "status": model.status,
        "ksValue": model.ks_value,
        "badRate": model.bad_rate,
        "accuracy": model.accuracy,
        "recall": model.recall,
        "precision": model.precision,
        "createTime": model.created_at.strftime("%Y-%m-%d %H:%M:%S") if model.created_at else None,
        "updateTime": model.updated_at.strftime("%Y-%m-%d %H:%M:%S") if model.updated_at else None,
        "description": model.description,
        "technicalDetails": model.technical_details
    }


async def set_current_model(model_id: int) -> Dict[str, Any]:
    """设置当前使用的模型"""
    # 检查模型是否存在
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    # 确保ai目录存在
    ai_dir = os.path.join(os.getcwd(), "ai")
    if not os.path.exists(ai_dir):
        os.makedirs(ai_dir)

    # 源文件路径
    original_file_path = os.path.join(os.getcwd(), model.file_path.lstrip('/'))
    if not os.path.exists(original_file_path):
        raise HTTPException(status_code=404, detail="模型文件不存在")
    

    # 构建目标文件路径
    target_file_path = os.path.join(ai_dir, "best_model_a.pth")

    # 复制文件
    shutil.copy(original_file_path, target_file_path)

    # 将之前的current模型设置为active
    await AIModel.filter(status="current").update(status="active")

    # 设置指定模型为current
    await AIModel.filter(id=model_id).update(status="current")

    return {
        "id": model_id,
        "status": "current"
    }



async def get_model_statistics() -> Dict[str, Any]:
    """获取模型统计信息"""
    # 获取当前模型
    current_model = await AIModel.get_or_none(status="current")
    current_model_data = None
    
    if current_model:
        current_model_data = {
            "id": current_model.id,
            "name": current_model.name,
            "version": current_model.version,
            "status": current_model.status,
            "ksValue": current_model.ks_value,
            "badRate": current_model.bad_rate,
            "accuracy": current_model.accuracy
        }
    
    # 获取各状态的模型数量
    total_models = await AIModel.all().count()
    active_models = await AIModel.filter(status="active").count()
    testing_models = await AIModel.filter(status="testing").count()
    
    return {
        "currentModel": current_model_data,
        "totalModels": total_models,
        "activeModels": active_models,
        "testingModels": testing_models
    }


async def get_current_model() -> Dict[str, Any]:
    """获取当前使用的模型"""
    model = await AIModel.get_or_none(status="current")
    if not model:
        raise HTTPException(status_code=404, detail="未设置当前模型")
    
    return {
        "id": model.id,
        "name": model.name,
        "version": model.version,
        "status": model.status,
        "ksValue": model.ks_value,
        "badRate": model.bad_rate,
        "accuracy": model.accuracy,
        "recall": model.recall,
        "precision": model.precision,
        "createTime": model.created_at.strftime("%Y-%m-%d %H:%M:%S") if model.created_at else None,
        "updateTime": model.updated_at.strftime("%Y-%m-%d %H:%M:%S") if model.updated_at else None,
        "description": model.description,
        "technicalDetails": model.technical_details
    }


async def delete_model(model_id: int) -> Dict[str, Any]:
    """删除模型"""
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    # 不能删除当前使用的模型
    if model.status == "current":
        raise HTTPException(status_code=400, detail="不能删除当前使用的模型")
    
    # 删除文件
    if os.path.exists(model.file_path):
        os.remove(model.file_path)
    
    # 删除数据库记录
    await model.delete()
    
    return {"id": model_id}


async def update_model(model_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """更新模型信息"""
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    # 更新字段
    for field, value in update_data.items():
        if hasattr(model, field) and value is not None:
            setattr(model, field, value)
    
    await model.save()
    
    return {
        "id": model.id,
        "name": model.name,
        "version": model.version,
        "description": model.description,
        "updateTime": model.updated_at.strftime("%Y-%m-%d %H:%M:%S") if model.updated_at else None
    }


async def update_model_metrics(model_id: int, metrics: Dict[str, float]) -> Dict[str, Any]:
    """更新模型指标"""
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    # 更新指标
    for metric, value in metrics.items():
        if hasattr(model, metric) and value is not None:
            setattr(model, metric, value)
    
    await model.save()
    
    return {
        "ksValue": model.ks_value,
        "badRate": model.bad_rate,
        "accuracy": model.accuracy,
        "recall": model.recall,
        "precision": model.precision
    }


async def refresh_model_metrics(model_id: int) -> Dict[str, Any]:
    """刷新模型指标"""
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    # 这里应该触发实际的模型指标计算
    # 现在返回模拟的刷新结果
    return {"refreshed": True}


async def get_model_file_path(model_id: int) -> str:
    """获取模型文件路径（用于下载）"""
    model = await AIModel.get_or_none(id=model_id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    
    if not os.path.exists(model.file_path):
        raise HTTPException(status_code=404, detail="模型文件不存在")
    
    return model.file_path
