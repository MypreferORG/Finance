# -*- coding: utf-8 -*-
"""
短信相关的数据模型定义
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SmsItem(BaseModel):
    """单条短信数据"""
    telphone: str = Field(..., description="手机号码")
    content: str = Field(..., description="短信内容")
    type: str = Field(..., description="短信类型: 1接收/2发送")
    sendDate: str = Field(..., description="发送时间")


class DeviceInfo(BaseModel):
    """设备信息"""
    brand: Optional[str] = Field(None, description="设备品牌")
    model: Optional[str] = Field(None, description="设备型号")
    system: Optional[str] = Field(None, description="操作系统")


class SmsAnalysisRequest(BaseModel):
    """短信风控分析请求"""
    sms_list: List[SmsItem] = Field(..., description="短信列表")
    device_info: Optional[DeviceInfo] = Field(None, description="设备信息")


class SmsAnalysisResponse(BaseModel):
    """短信风控分析响应"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: Dict[str, Any] = Field(..., description="风控分析结果")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "success",
                "data": {
                    "final_decision": "REJECT",
                    "risk_tags": ["外部违约", "多头借贷"],
                    "analysis_summary": "发现用户存在严重逾期记录",
                    "raw_risk_count": 5
                }
            }
        }
