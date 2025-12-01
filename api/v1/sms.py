# -*- coding: utf-8 -*-
"""
# @Create on : 2025/12/01
# @Author : Copilot
# @Des: 短信风控接口
"""

from fastapi import APIRouter, Depends, HTTPException
from schemas.sms import SmsAnalysisRequest, SmsAnalysisResponse
from services.sms_risk_service import SmsRiskService
from core.dependences import user_required
from models import UserAuth
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sms", summary="短信风控分析", response_model=SmsAnalysisResponse)
async def analyze_sms(
    request: SmsAnalysisRequest,
    user: UserAuth = Depends(user_required)
):
    """
    短信风控分析接口
    
    客户端发送短信数据，系统进行风控识别分析
    
    Args:
        request: 包含短信列表和设备信息的请求体
        user: 当前认证用户
        
    Returns:
        风控分析结果，包括决策、风险标签、分析摘要等
    """
    try:
        # 记录用户请求
        logger.info(f"用户 {user.id} 请求短信风控分析，短信数量: {len(request.sms_list)}")
        
        # 验证短信列表不为空
        if not request.sms_list:
            raise HTTPException(status_code=400, detail="短信列表不能为空")
        
        # 转换为字典格式供风控引擎使用
        sms_data = [sms.dict() for sms in request.sms_list]
        device_data = request.device_info.dict() if request.device_info else None
        
        # 调用风控服务
        risk_result = SmsRiskService.analyze_sms_risk(sms_data, device_data)
        
        # 格式化响应
        formatted_data = SmsRiskService.format_response(risk_result)
        
        # 记录风控决策
        logger.info(f"用户 {user.id} 风控决策: {formatted_data.get('final_decision')}")
        
        return SmsAnalysisResponse(
            code=200,
            message="分析完成",
            data=formatted_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"短信风控分析失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"风控分析失败: {str(e)}")
