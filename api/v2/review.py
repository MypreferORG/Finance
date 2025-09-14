# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/27
# @Author : Myprefer
# @Des: 复审管理API
"""

from fastapi import APIRouter, HTTPException, Query, Path
from schemas.review import (
    ReviewApplicationListResponse, ReviewApplicationDetailResponse,
    ReviewProcessRequest, BatchReviewProcessRequest, ReviewStatsResponse,
    ReviewHistoryResponse, BaseResponse
)
from services.review_service import (
    get_review_applications, get_review_application_detail,
    process_review_application, batch_process_review_applications,
    get_review_statistics, get_review_history
)
from typing import Optional

router = APIRouter()


@router.get("/applications", response_model=ReviewApplicationListResponse)
async def get_review_application_list(
    pageNo: int = Query(1, description="页码"),
    pageSize: int = Query(10, description="每页条数"),
    status: Optional[str] = Query(None, description="复审状态筛选"),
    priority: Optional[str] = Query(None, description="优先级筛选"),
    keyword: Optional[str] = Query(None, description="关键词搜索")
):
    """获取复审申请列表"""
    try:
        data = await get_review_applications(pageNo, pageSize, status, priority, keyword)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取复审申请列表失败: {str(e)}")


@router.get("/application/{application_id}", response_model=ReviewApplicationDetailResponse)
async def get_review_application_detail_api(
    application_id: int = Path(..., description="复审申请ID")
):
    """获取复审申请详情"""
    try:
        data = await get_review_application_detail(application_id)
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"获取复审申请详情失败: {str(e)}")


@router.post("/process/{application_id}", response_model=BaseResponse)
async def process_review(
    application_id: int = Path(..., description="复审申请ID"),
    request: ReviewProcessRequest = None
):
    """复审审批"""
    try:
        if not request:
            raise HTTPException(status_code=400, detail="请求参数不能为空")
        
        data = await process_review_application(
            application_id=application_id,
            result=request.result,
            comment=request.comment,
            auditor=request.auditor
        )
        return {
            "success": True,
            "code": 200,
            "message": data.get("message", "操作成功"),
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"复审处理失败: {str(e)}")


@router.post("/batch-process", response_model=BaseResponse)
async def batch_process_review(request: BatchReviewProcessRequest):
    """批量处理复审申请"""
    try:
        data = await batch_process_review_applications(
            application_ids=request.ids,
            result=request.result,
            comment=request.comment,
            auditor=request.auditor
        )
        return {
            "success": True,
            "code": 200,
            "message": "批量处理完成",
            "data": data
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"批量处理失败: {str(e)}")


@router.get("/stats", response_model=ReviewStatsResponse)
async def get_review_stats():
    """获取复审统计数据"""
    try:
        data = await get_review_statistics()
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取复审统计失败: {str(e)}")


@router.get("/history", response_model=ReviewHistoryResponse)
async def get_review_history_api(
    pageNo: int = Query(1, description="页码"),
    pageSize: int = Query(10, description="每页条数"),
    status: Optional[str] = Query(None, description="复审结果筛选：review_approved/review_rejected"),
    auditor: Optional[str] = Query(None, description="复审员姓名"),
    keyword: Optional[str] = Query(None, description="关键词搜索（申请人姓名、电话）"),
    startTime: Optional[str] = Query(None, description="开始时间 (YYYY-MM-DD)"),
    endTime: Optional[str] = Query(None, description="结束时间 (YYYY-MM-DD)")
):
    """获取复审历史记录"""
    try:
        data = await get_review_history(
            page_no=pageNo,
            page_size=pageSize,
            status=status,
            auditor=auditor,
            keyword=keyword,
            start_time=startTime,
            end_time=endTime
        )
        return {
            "success": True,
            "code": 200,
            "message": "操作成功",
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取复审历史记录失败: {str(e)}")
