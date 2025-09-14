# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/27
# @Author : Myprefer
# @Des: 模型管理API
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Path
from fastapi.responses import FileResponse
from schemas.model import (
    ModelUploadResponse, ModelListResponse, ModelStatisticsResponse,
    ModelUpdateRequest, ModelMetricsRequest, BaseResponse
)
from services.model_management_service import (
    upload_model_file, get_model_list, get_model_detail, set_current_model,
    get_model_statistics, get_current_model, delete_model, update_model,
    update_model_metrics, refresh_model_metrics,
    get_model_file_path
)
from typing import Optional
import os

router = APIRouter()


@router.post("/upload", response_model=ModelUploadResponse)
async def upload_model(
    file: UploadFile = File(...),
    name: str = Form(...),
    version: str = Form(...),
    description: str = Form(...),
    ksValue: float = Form(...),
    badRate: float = Form(...),
    accuracy: float = Form(...),
    recall: float = Form(...),
    precision: float = Form(...),
    technicalDetails: Optional[str] = Form(None)
):
    """
    上传模型文件
    
    - **file**: 模型文件（支持.pth, .ckpt, .pkl, .h5, .pb, .onnx, .joblib）
    - **name**: 模型名称
    - **version**: 版本号
    - **description**: 模型描述
    - **ksValue**: K-S值 (0-1之间)
    - **badRate**: 坏账率 (0-1之间)
    - **accuracy**: 准确率 (0-1之间)
    - **recall**: 召回率 (0-1之间)
    - **precision**: 精确率 (0-1之间)
    - **technicalDetails**: 技术细节（可选）
    """
    try:
        # 验证性能指标范围
        metrics = {
            "ksValue": ksValue,
            "badRate": badRate,
            "accuracy": accuracy,
            "recall": recall,
            "precision": precision
        }
        
        for metric_name, value in metrics.items():
            if not (0 <= value <= 1):
                raise HTTPException(
                    status_code=400,
                    detail=f"{metric_name} 必须在0-1之间，当前值: {value}"
                )
        
        result = await upload_model_file(
            file=file,
            name=name,
            version=version,
            description=description,
            technical_details=technicalDetails,
            metrics=metrics
        )
        return {
            "success": True,
            "code": 200,
            "message": "模型上传成功",
            "data": result
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"模型上传失败: {str(e)}")


@router.get("/list", response_model=ModelListResponse)
async def get_models(
    pageNo: int = Query(1, description="页码"),
    pageSize: int = Query(10, description="每页条数"),
    status: Optional[str] = Query(None, description="模型状态筛选"),
    name: Optional[str] = Query(None, description="模型名称模糊搜索")
):
    """获取模型列表"""
    try:
        data = await get_model_list(pageNo, pageSize, status, name)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")


@router.get("/{model_id}", response_model=BaseResponse)
async def get_model(model_id: int = Path(..., description="模型ID")):
    """获取模型详情"""
    try:
        data = await get_model_detail(model_id)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"获取模型详情失败: {str(e)}")


@router.put("/{model_id}/set-current", response_model=BaseResponse)
async def set_model_current(model_id: int = Path(..., description="模型ID")):
    """设置当前使用模型"""
    try:
        data = await set_current_model(model_id)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"设置当前模型失败: {str(e)}")
    



@router.get("/statistics", response_model=ModelStatisticsResponse)
async def get_statistics():
    """获取模型性能统计"""
    try:
        data = await get_model_statistics()
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型统计失败: {str(e)}")


@router.get("/current", response_model=BaseResponse)
async def get_current():
    """获取当前使用的模型信息"""
    try:
        data = await get_current_model()
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"获取当前模型失败: {str(e)}")


@router.delete("/{model_id}", response_model=BaseResponse)
async def delete_model_api(model_id: int = Path(..., description="模型ID")):
    """删除模型"""
    try:
        data = await delete_model(model_id)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"删除模型失败: {str(e)}")


@router.put("/{model_id}", response_model=BaseResponse)
async def update_model_info(
    model_id: int = Path(..., description="模型ID"),
    request: ModelUpdateRequest = None
):
    """更新模型信息"""
    try:
        update_data = request.dict(exclude_unset=True) if request else {}
        data = await update_model(model_id, update_data)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"更新模型信息失败: {str(e)}")


@router.get("/{model_id}/metrics", response_model=BaseResponse)
async def get_model_metrics(model_id: int = Path(..., description="模型ID")):
    """获取指定模型的性能指标"""
    try:
        model_detail = await get_model_detail(model_id)
        metrics = {
            "ksValue": model_detail.get("ksValue"),
            "badRate": model_detail.get("badRate"),
            "accuracy": model_detail.get("accuracy"),
            "recall": model_detail.get("recall"),
            "precision": model_detail.get("precision")
        }
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": metrics
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"获取模型指标失败: {str(e)}")


@router.put("/{model_id}/metrics", response_model=BaseResponse)
async def update_metrics(
    model_id: int = Path(..., description="模型ID"),
    request: ModelMetricsRequest = None
):
    """更新模型指标"""
    try:
        metrics = request.dict(exclude_unset=True) if request else {}
        data = await update_model_metrics(model_id, metrics)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"更新模型指标失败: {str(e)}")


@router.post("/refresh-metrics", response_model=BaseResponse)
async def refresh_metrics(request: dict):
    """刷新模型指标"""
    try:
        model_id = request.get("modelId")
        if not model_id:
            raise HTTPException(status_code=400, detail="缺少模型ID")
        
        data = await refresh_model_metrics(model_id)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"刷新模型指标失败: {str(e)}")


@router.get("/{model_id}/download")
async def download_model(model_id: int = Path(..., description="模型ID")):
    """下载模型文件"""
    try:
        file_path = await get_model_file_path(model_id)
        filename = os.path.basename(file_path)
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"下载模型文件失败: {str(e)}")
