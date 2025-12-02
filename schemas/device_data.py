# -*- coding: utf-8 -*-
"""
# @Create on : 2025/12/02
# @Author : Copilot
# @Des: 设备数据相关的数据模型定义（短信、应用、通讯录、图片）
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============= 短信相关 =============
class SmsItem(BaseModel):
    """单条短信数据"""
    telphone: Optional[str] = Field(None, description="发送者号码")
    content: str = Field(..., description="短信内容")
    type: Optional[str] = Field("1", description="短信类型: 1接收/2发送")
    sendDate: Optional[str] = Field(None, description="发送时间")


# ============= 应用列表相关 =============
class AppItem(BaseModel):
    """单个应用数据"""
    name: str = Field(..., description="应用名称")
    pkg_name: Optional[str] = Field(None, description="包名")
    version_name: Optional[str] = Field(None, description="版本名")
    version_code: Optional[int] = Field(None, description="版本号")
    is_system_app: Optional[bool] = Field(False, description="是否系统应用")
    install_time: Optional[str] = Field(None, description="安装时间")
    last_update_time: Optional[str] = Field(None, description="最后更新时间")


# ============= 通讯录相关 =============
class ContactItem(BaseModel):
    """单个联系人数据"""
    display_name: Optional[str] = Field(None, description="联系人姓名")
    phone_number: str = Field(..., description="电话号码")
    phone_number_raw: Optional[str] = Field(None, description="原始电话号码")
    phone_type: Optional[str] = Field(None, description="号码类型: mobile/home/work等")


# ============= 图片相关 =============
class ImageItem(BaseModel):
    """单张图片数据"""
    image_type: str = Field(..., description="图片类型: id_card_front/id_card_back/face/other")
    image_url: Optional[str] = Field(None, description="图片URL或路径")
    image_data: Optional[str] = Field(None, description="图片Base64数据(可选)")


# ============= 设备信息 =============
class DeviceInfo(BaseModel):
    """设备信息"""
    brand: Optional[str] = Field(None, description="设备品牌")
    model: Optional[str] = Field(None, description="设备型号")
    system: Optional[str] = Field(None, description="操作系统")
    os_version: Optional[str] = Field(None, description="系统版本")
    device_id: Optional[str] = Field(None, description="设备唯一标识")


# ============= 请求模型 =============
class DeviceDataRequest(BaseModel):
    """设备数据上传请求"""
    sms_list: Optional[List[SmsItem]] = Field(None, description="短信列表")
    app_list: Optional[List[AppItem]] = Field(None, description="应用列表")
    contact_list: Optional[List[ContactItem]] = Field(None, description="通讯录列表")
    image_list: Optional[List[ImageItem]] = Field(None, description="图片列表")
    device_info: Optional[DeviceInfo] = Field(None, description="设备信息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sms_list": [
                    {"telphone": "10086", "content": "您的话费余额不足", "type": "1", "sendDate": "2025-12-01 10:30:00"}
                ],
                "app_list": [
                    {"name": "微信", "pkg_name": "com.tencent.mm", "version_name": "8.0.0"}
                ],
                "contact_list": [
                    {"display_name": "张三", "phone_number": "13800138000"}
                ],
                "device_info": {
                    "brand": "Xiaomi",
                    "model": "Mi 11",
                    "system": "Android"
                }
            }
        }


# ============= 响应模型 =============
class DeviceDataResponse(BaseModel):
    """设备数据上传响应"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="响应消息")
    data: Dict[str, Any] = Field(..., description="上传结果详情")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "message": "数据上传成功",
                "data": {
                    "batch_id": "batch_20251202_abc123",
                    "sms_count": 10,
                    "app_count": 50,
                    "contact_count": 100,
                    "image_count": 2
                }
            }
        }
