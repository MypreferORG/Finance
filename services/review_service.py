# -*- coding: utf-8 -*-
"""
# @Create on : 2025/06/27
# @Author : Myprefer
# @Des: 复审管理服务
"""

from fastapi import HTTPException
from models.review import ReviewApplication
from models.loan import LoanRecord
from typing import List, Optional, Dict, Any
from datetime import datetime
from tortoise.expressions import Q


async def get_review_applications(
    page_no: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    keyword: Optional[str] = None
) -> Dict[str, Any]:
    """获取复审申请列表"""
    
    # 构建查询条件
    query = ReviewApplication.all()
    
    if status:
        query = query.filter(status=status)
    
    if priority:
        query = query.filter(priority=priority)
    
    if keyword:
        query = query.filter(
            Q(applicant_name__icontains=keyword) |
            Q(phone__icontains=keyword) |
            Q(review_reason__icontains=keyword)
        )
    
    # 获取总数
    total = await query.count()
    
    # 分页查询
    offset = (page_no - 1) * page_size
    applications = await query.offset(offset).limit(page_size).order_by('-review_apply_time')
    
    # 转换为响应格式
    records = []
    for app in applications:
        records.append({
            "id": app.id,
            "original_audit_id": app.original_audit_id,
            "applicant_name": app.applicant_name,
            "phone": app.phone,
            "id_card": app.id_card,
            "loan_amount": float(app.loan_amount),
            "loan_purpose": app.loan_purpose,
            "original_result": app.original_result,
            "original_reason": app.original_reason,
            "original_auditor": app.original_auditor,
            "original_audit_time": app.original_audit_time.strftime("%Y-%m-%d %H:%M:%S") if app.original_audit_time else None,
            "review_reason": app.review_reason,
            "review_apply_time": app.review_apply_time.strftime("%Y-%m-%d %H:%M:%S") if app.review_apply_time else None,
            "status": app.status,
            "priority": app.priority,
            "additional_docs": app.additional_docs or [],
            "review_auditor": app.review_auditor,
            "review_time": app.review_time.strftime("%Y-%m-%d %H:%M:%S") if app.review_time else None,
            "review_result": app.review_result,
            "review_comment": app.review_comment
        })
    
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "records": records,
        "total": total,
        "pageNo": page_no,
        "pageSize": page_size,
        "totalPages": total_pages
    }


async def get_review_application_detail(application_id: int) -> Dict[str, Any]:
    """获取复审申请详情"""
    
    # 获取复审申请
    application = await ReviewApplication.get_or_none(id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="复审申请不存在")
    
    # 获取原始申请信息
    original_application = await LoanRecord.get_or_none(id=application.original_audit_id)
    
    # 构建响应数据
    detail_data = {
        "id": application.id,
        "original_audit_id": application.original_audit_id,
        "applicant_name": application.applicant_name,
        "phone": application.phone,
        "id_card": application.id_card,
        "loan_amount": float(application.loan_amount),
        "loan_purpose": application.loan_purpose,
        "original_result": application.original_result,
        "original_reason": application.original_reason,
        "original_auditor": application.original_auditor,
        "original_audit_time": application.original_audit_time.strftime("%Y-%m-%d %H:%M:%S") if application.original_audit_time else None,
        "review_reason": application.review_reason,
        "review_apply_time": application.review_apply_time.strftime("%Y-%m-%d %H:%M:%S") if application.review_apply_time else None,
        "status": application.status,
        "priority": application.priority,
        "additional_docs": application.additional_docs or [],
        "review_auditor": application.review_auditor,
        "review_time": application.review_time.strftime("%Y-%m-%d %H:%M:%S") if application.review_time else None,
        "review_result": application.review_result,
        "review_comment": application.review_comment
    }
    
    # 添加原始申请信息
    if original_application:
        # 获取关联的用户信息
        await original_application.fetch_related('user')
        user = original_application.user
        
        # 尝试获取用户详细信息
        user_profile = None
        try:
            user_profile = await user.user_profiles.first() if user else None
        except:
            pass
        
        detail_data["original_application"] = {
            "id": original_application.id,
            "applicant_name": user_profile.full_name if user_profile and user_profile.full_name else (user.username if user else "未知"),
            "phone": user_profile.phone_number if user_profile else (user.phone_number if user else "未知"),
            "id_card": user_profile.id_card_number if user_profile else "未知",
            "loan_amount": float(original_application.amount),
            "loan_purpose": original_application.usage,
            "income": float(getattr(original_application, 'income', 0)) if hasattr(original_application, 'income') and getattr(original_application, 'income') else (float(user_profile.income) if user_profile and user_profile.income else None),
            "credit_score": getattr(original_application, 'credit_score', None),
            "apply_time": original_application.created_at.strftime("%Y-%m-%d %H:%M:%S") if original_application.created_at else None,
            "status": original_application.status,
            "audit_time": getattr(original_application, 'audit_time', original_application.updated_at).strftime("%Y-%m-%d %H:%M:%S") if getattr(original_application, 'audit_time', original_application.updated_at) else None,
            "auditor": getattr(original_application, 'auditor', '系统审核'),
            "remark": getattr(original_application, 'remark', '暂无备注')
        }
    
    return detail_data


async def process_review_application(
    application_id: int,
    result: str,
    comment: str,
    auditor: str
) -> Dict[str, Any]:
    """处理复审申请"""
    
    # 获取复审申请
    application = await ReviewApplication.get_or_none(id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="复审申请不存在")
    
    # 检查状态
    if application.status != "review_pending":
        raise HTTPException(status_code=400, detail="该复审申请已被处理")
    
    # 更新复审申请状态
    new_status = "review_approved" if result == "approved" else "review_rejected"
    
    application.status = new_status
    application.review_result = result
    application.review_comment = comment
    application.review_auditor = auditor
    application.review_time = datetime.now()
    
    await application.save()
    
    # 如果复审通过，需要更新原始申请状态
    if result == "approved":
        original_application = await LoanRecord.get_or_none(id=application.original_audit_id)
        if original_application:
            original_application.status = "approved"  # 或者其他适当的状态
            await original_application.save()
    
    message = "复审通过成功" if result == "approved" else "复审拒绝成功"
    
    return {
        "id": application_id,
        "result": result,
        "message": message
    }


async def batch_process_review_applications(
    application_ids: List[int],
    result: str,
    comment: str,
    auditor: str
) -> Dict[str, Any]:
    """批量处理复审申请"""
    
    processed_count = 0
    
    for app_id in application_ids:
        try:
            await process_review_application(app_id, result, comment, auditor)
            processed_count += 1
        except Exception:
            # 记录错误但继续处理其他申请
            continue
    
    return {
        "processedCount": processed_count
    }


async def get_review_statistics() -> Dict[str, Any]:
    """获取复审统计数据"""
    
    # 获取各种统计数据
    total_count = await ReviewApplication.all().count()
    pending_count = await ReviewApplication.filter(status="review_pending").count()
    approved_count = await ReviewApplication.filter(status="review_approved").count()
    rejected_count = await ReviewApplication.filter(status="review_rejected").count()
    
    # 计算通过率
    processed_count = approved_count + rejected_count
    approval_rate = (approved_count / processed_count * 100) if processed_count > 0 else 0
    
    # 今日处理数量
    today = datetime.now().date()
    today_count = await ReviewApplication.filter(
        review_time__gte=today,
        status__in=["review_approved", "review_rejected"]
    ).count()
    
    # 平均处理时长（简化计算，实际可以更精确）
    avg_review_time = 2.3  # 模拟数据，实际应该从数据库计算
    
    return {
        "totalReviewCount": total_count,
        "pendingReviewCount": pending_count,
        "approvedReviewCount": approved_count,
        "rejectedReviewCount": rejected_count,
        "reviewApprovalRate": round(approval_rate, 1),
        "avgReviewTime": avg_review_time,
        "todayReviewCount": today_count
    }


async def get_review_history(
    page_no: int = 1,
    page_size: int = 10,
    status: Optional[str] = None,
    auditor: Optional[str] = None,
    keyword: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> Dict[str, Any]:
    """获取复审历史记录"""
    
    # 构建查询条件 - 只查询已处理的复审申请
    query = ReviewApplication.filter(status__in=["review_approved", "review_rejected"])
    
    if status:
        query = query.filter(status=status)
    
    if auditor:
        query = query.filter(review_auditor__icontains=auditor)
    
    if keyword:
        query = query.filter(
            Q(applicant_name__icontains=keyword) |
            Q(phone__icontains=keyword)
        )
    
    # 时间范围筛选
    if start_time:
        try:
            start_date = datetime.strptime(start_time, "%Y-%m-%d").date()
            query = query.filter(review_time__gte=start_date)
        except ValueError:
            pass  # 忽略无效的日期格式
    
    if end_time:
        try:
            end_date = datetime.strptime(end_time, "%Y-%m-%d").date()
            # 加上一天以包含整个结束日期
            from datetime import timedelta
            end_date_plus_one = end_date + timedelta(days=1)
            query = query.filter(review_time__lt=end_date_plus_one)
        except ValueError:
            pass  # 忽略无效的日期格式
    
    # 获取总数
    total = await query.count()
    
    # 分页查询，按处理时间倒序排列
    offset = (page_no - 1) * page_size
    applications = await query.offset(offset).limit(page_size).order_by('-review_time')
    
    # 转换为响应格式
    records = []
    for app in applications:
        # 计算处理时长（天）
        process_duration = None
        if app.review_time and app.review_apply_time:
            time_diff = app.review_time - app.review_apply_time
            process_duration = round(time_diff.total_seconds() / (24 * 3600), 1)  # 转换为天数，保留1位小数
        
        records.append({
            "id": app.id,
            "original_audit_id": app.original_audit_id,
            "applicant_name": app.applicant_name,
            "phone": app.phone,
            "id_card": app.id_card,
            "loan_amount": float(app.loan_amount),
            "loan_purpose": app.loan_purpose,
            "original_result": app.original_result,
            "original_reason": app.original_reason,
            "original_auditor": app.original_auditor,
            "original_audit_time": app.original_audit_time.strftime("%Y-%m-%d %H:%M:%S") if app.original_audit_time else None,
            "review_reason": app.review_reason,
            "review_apply_time": app.review_apply_time.strftime("%Y-%m-%d %H:%M:%S") if app.review_apply_time else None,
            "status": app.status,
            "priority": app.priority,
            "additional_docs": app.additional_docs or [],
            "review_auditor": app.review_auditor,
            "review_time": app.review_time.strftime("%Y-%m-%d %H:%M:%S") if app.review_time else None,
            "review_result": app.review_result,
            "review_comment": app.review_comment,
            "process_duration": process_duration
        })
    
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "records": records,
        "total": total,
        "pageNo": page_no,
        "pageSize": page_size,
        "totalPages": total_pages
    }
