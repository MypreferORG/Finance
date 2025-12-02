# -*- coding: utf-8 -*-
"""
# @Create on : 2025/11/13
# @Author : Jason
# @Des: 黑名单（App 与 电话）增删查 + 检测接口
"""
from typing import Optional, List
import re
from fastapi import APIRouter, HTTPException, Query
from tortoise.exceptions import IntegrityError

from models import AppBlacklist, CallBlacklist
from schemas.blacklist import (
    AppBlacklistCreateRequest, AppBlacklistResponse, AppBlacklistListResponse,
    CallBlacklistCreateRequest, CallBlacklistResponse, CallBlacklistListResponse,
    DeleteSuccessResponse, AppInfoCheckRequest, ContactInfoCheckRequest,
    SmsBatchCheckRequest, SmsCheckResponse
)
from utils.message_retrieval import comprehensive_risk_analysis

router = APIRouter()

# ------------------ App 黑名单 ------------------
@router.post("/app", summary="添加应用黑名单", response_model=AppBlacklistResponse)
async def add_app_blacklist(data: AppBlacklistCreateRequest):
    try:
        obj = await AppBlacklist.create(name=data.name)
        return obj
    except IntegrityError:
        raise HTTPException(status_code=400, detail="应用已在黑名单中或名称重复")

@router.get("/app/list", summary="查询应用黑名单列表（分页）", response_model=AppBlacklistListResponse)
async def list_app_blacklist(
    search: Optional[str] = Query(None, description="按名称包含搜索"),
    pageNo: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
):
    qs = AppBlacklist.all()
    if search:
        qs = qs.filter(name__icontains=search)
    total = await qs.count()
    offset = (pageNo - 1) * pageSize
    records = await qs.order_by('-id').offset(offset).limit(pageSize)
    return AppBlacklistListResponse(total=total, pageNo=pageNo, pageSize=pageSize, records=records)

@router.delete("/app/{item_id}", summary="删除应用黑名单项", response_model=DeleteSuccessResponse)
async def delete_app_blacklist(item_id: int):
    obj = await AppBlacklist.get_or_none(id=item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="该记录不存在")
    await obj.delete()
    return DeleteSuccessResponse(success=True, message="删除成功")

@router.get("/app/exists", summary="按名称检测应用是否在黑名单", response_model=bool)
async def app_exists(name: str = Query(..., description="应用名称")):
    exists = await AppBlacklist.filter(name__iexact=name.strip()).exists()
    return exists

@router.post("/app/check_batch", summary="批量检测应用是否存在黑名单(任一命中即 True)", response_model=bool)
async def app_check_batch(apps: List[AppInfoCheckRequest]):
    if not apps:
        return False
    # 提取 name 并去除空串
    names = [i.name.strip() for i in apps if i.name and i.name.strip()]
    if not names:
        return False
    # 逐个 iexact 命中即可（可优化为 IN + 规范化表结构，这里保持简单）
    # 使用 __in 无法直接配合 iexact，因此采用 OR 链接
    from tortoise.expressions import Q
    cond = None
    for n in names:
        q = Q(name__iexact=n)
        cond = q if cond is None else (cond | q)
    exists = await AppBlacklist.filter(cond).exists() if cond is not None else False
    return exists

# ------------------ 电话黑名单 ------------------
@router.post("/call", summary="添加电话黑名单", response_model=CallBlacklistResponse)
async def add_call_blacklist(data: CallBlacklistCreateRequest):
    try:
        # 号码归一化，只存数字
        norm = re.sub(r"\D", "", data.phone_number)
        obj = await CallBlacklist.create(phone_number=norm)
        return obj
    except IntegrityError:
        raise HTTPException(status_code=400, detail="电话号码已在黑名单中或重复")

@router.get("/call/list", summary="查询电话黑名单列表（分页）", response_model=CallBlacklistListResponse)
async def list_call_blacklist(
    search: Optional[str] = Query(None, description="按号码包含搜索(会自动去除非数字字符)"),
    pageNo: int = Query(1, ge=1),
    pageSize: int = Query(10, ge=1, le=100),
):
    qs = CallBlacklist.all()
    if search:
        norm = re.sub(r"\D", "", search)
        qs = qs.filter(phone_number__icontains=norm)
    total = await qs.count()
    offset = (pageNo - 1) * pageSize
    records = await qs.order_by('-id').offset(offset).limit(pageSize)
    return CallBlacklistListResponse(total=total, pageNo=pageNo, pageSize=pageSize, records=records)

@router.delete("/call/{item_id}", summary="删除电话黑名单项", response_model=DeleteSuccessResponse)
async def delete_call_blacklist(item_id: int):
    obj = await CallBlacklist.get_or_none(id=item_id)
    if not obj:
        raise HTTPException(status_code=404, detail="该记录不存在")
    await obj.delete()
    return DeleteSuccessResponse(success=True, message="删除成功")

@router.get("/call/exists", summary="按号码检测是否在黑名单", response_model=bool)
async def call_exists(phone: str = Query(..., description="电话号码，允许包含分隔符")):
    norm = re.sub(r"\D", "", phone)
    exists = await CallBlacklist.filter(phone_number=norm).exists()
    return exists

@router.post("/call/check_contacts", summary="批量检测联系人是否包含黑名单号码(任一命中即 True)", response_model=bool)
async def call_check_contacts(contacts: List[ContactInfoCheckRequest]):
    if not contacts:
        return False
    numbers: List[str] = []
    for c in contacts:
        if not c or not c.phoneNumbers:
            continue
        for item in c.phoneNumbers:
            if item and item.value:
                numbers.append(re.sub(r"\D", "", item.value))
    numbers = [n for n in numbers if n]
    if not numbers:
        return False
    exists = await CallBlacklist.filter(phone_number__in=list(set(numbers))).exists()
    return exists


# ------------------ 短信风险检测 ------------------
@router.post("/sms/check", summary="短信风险检测(Embedding+LLM)", response_model=SmsCheckResponse)
async def sms_risk_check(data: SmsBatchCheckRequest):
    """
    短信风险检测接口
    - 使用 Embedding 粗筛 + Qwen LLM 精判
    - 返回风险决策和详细分析
    """
    if not data.sms_list:
        return SmsCheckResponse(
            hit=False,
            risk_score=0.0,
            final_decision="PASS",
            risk_tags=[],
            analysis_summary="无短信数据"
        )
    
    # 转换为工具函数需要的格式
    sms_data = [
        {
            "telphone": sms.telphone or "",
            "content": sms.content,
            "sendDate": sms.sendDate or ""
        }
        for sms in data.sms_list
    ]
    
    # 调用风控分析
    result = comprehensive_risk_analysis(sms_data)
    
    decision = result.get("final_decision", "PASS")
    
    # 决策映射到风险分数
    decision_score_map = {
        "PASS": 0.0,
        "LOWER_SCORE": 0.4,
        "LOWER_LIMIT": 0.5,
        "MANUAL_REVIEW": 0.7,
        "REJECT": 1.0
    }
    risk_score = decision_score_map.get(decision, 0.5)
    
    return SmsCheckResponse(
        hit=decision != "PASS",
        risk_score=risk_score,
        final_decision=decision,
        risk_tags=result.get("risk_tags", []),
        analysis_summary=result.get("analysis_summary"),
        raw_risk_count=result.get("raw_risk_count", 0)
    )


@router.post("/sms/check_simple", summary="短信风险检测(简化版-仅返回是否命中)", response_model=bool)
async def sms_check_simple(data: SmsBatchCheckRequest):
    """
    短信风险检测简化接口
    - 返回 True 表示命中风险，False 表示通过
    """
    if not data.sms_list:
        return False
    
    sms_data = [
        {
            "telphone": sms.telphone or "",
            "content": sms.content,
            "sendDate": sms.sendDate or ""
        }
        for sms in data.sms_list
    ]
    
    result = comprehensive_risk_analysis(sms_data)
    decision = result.get("final_decision", "PASS")
    
    # PASS 表示未命中，其他都算命中
    return decision != "PASS"
