# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/18 下午10:45
# @Author : Jason
# @Des: 管理端 用户信息相关的schema模型
"""
from pydantic import BaseModel, Field, computed_field
from datetime import datetime, date
from typing import Optional, List, Any
from decimal import Decimal

class UserAuthResponse(BaseModel):
    """
    用户认证信息响应模型
    """
    id: str  # 唯一用户ID
    username: str  # 用户名
    phone_number: str  # 手机号
    role: str  # 用户角色 (user/admin/root)
    created_at: datetime  # 注册时间
    updated_at: datetime  # 信息更新时间

    class Config:
        # orm_mode = True
        from_attributes = True

class PaginatedUserData(BaseModel):
    """
    分页用户数据
    """
    total: int  # 总用户数
    pageNo: int  # 当前页码
    pageSize: int  # 每页数量
    records: List[UserAuthResponse]  # 当前页的用户认证信息列表

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedUserResponse(BaseModel):
    """
    带分页信息的用户认证响应数据
    """
    success: bool  # 请求是否成功
    data: PaginatedUserData  # 分页的用户数据

    class Config:
        # orm_mode = True
        from_attributes = True


class UserAuthFilterRequest(BaseModel):
    """
    用户认证信息筛选请求模型
    """
    username: Optional[str]  # 按用户名筛选
    phone_number: Optional[str]  # 按手机号筛选
    role: Optional[str]  # 按角色筛选 (user/admin/root)
    page: Optional[int] = 1  # 分页参数：页码，默认为第1页
    limit: Optional[int] = 10  # 分页参数：每页的数量，默认为10

    class Config:
        # orm_mode = True
        from_attributes = True


class UpdateUserAuthRequest(BaseModel):
    """
    更新用户认证信息的请求模型
    """
    username: Optional[str]  # 修改用户名
    phone_number: Optional[str]  # 修改手机号
    role: Optional[str]  # 修改角色 (user/admin/root)

    class Config:
        # orm_mode = True
        from_attributes = True


class UserSignLogResponse(BaseModel):
    """
    用户登录日志响应模型
    """
    id: int  # 日志ID
    user_id: int  # 用户ID
    action: str  # 操作类型 (登录/登出)
    ip_address: Optional[str]  # IP地址
    user_agent: Optional[str]  # 用户设备信息
    success: int  # 操作是否成功
    # todo 若为bool，无法在light2f显示
    message: Optional[str]  # 操作结果信息
    created_at: datetime  # 操作时间

    # # 添加 user 字段，但在序列化时排除
    # user: Any = Field(exclude=True)
    #
    # # 计算字段，提取 user_id
    # @computed_field
    # @property
    # def user_id(self) -> str:
    #     return str(self.user_id)

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedSignLogData(BaseModel):
    """
    分页用户登录日志数据
    """
    total: int  # 总记录数
    pageNo: int  # 当前页码
    pageSize: int  # 每页数量
    records: List[UserSignLogResponse]  # 当前页的用户登录日志列表

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedSignLogResponse(BaseModel):
    """
    带分页信息的用户登录日志响应数据
    """
    success: bool  # 请求是否成功
    data: PaginatedSignLogData  # 分页的登录日志数据

    class Config:
        # orm_mode = True
        from_attributes = True


class UserProfileResponse(BaseModel):
    """
    用户个人信息响应模型
    """
    id: int # 用户id
    username: str  # 用户名
    full_name: Optional[str]  # 姓名
    phone_number: str  # 电话号码
    gender: Optional[str]  # 性别
    id_card_number: Optional[str]  # 身份证号
    bank_account: Optional[str]  # 银行卡号
    address: Optional[str]  # 地址
    date_of_birth: Optional[date]  # 出生日期
    student_verified: Optional[int]  # 是否学生认证
    # todo bool无法在light2f显示
    profession: Optional[str]  # 职业
    income: Optional[Decimal]  # 月收入
    is_profile_completed: int  # 是否完善个人信息
    # todo bool无法在light2f显示
    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedUserProfileData(BaseModel):
    """
    分页用户个人信息数据
    """
    total: int  # 总记录数
    pageNo: int  # 当前页码
    pageSize: int  # 每页数量
    records: List[UserProfileResponse]  # 当前页的用户个人信息列表

    class Config:
        # orm_mode = True
        from_attributes = True


class PaginatedUserProfileResponse(BaseModel):
    """
    带分页信息的用户个人信息响应数据
    """
    success: bool  # 请求是否成功
    data: PaginatedUserProfileData  # 分页的用户个人信息数据

    class Config:
        # orm_mode = True
        from_attributes = True


class UpdateUserProfileRequest(BaseModel):
    """
    更新用户个人信息的请求模型
    """
    full_name: Optional[str] = Field(None, description="姓名")
    phone_number: Optional[str] = Field(None, description="手机号")
    gender: Optional[str] = Field(None, description="性别")
    address: Optional[str] = Field(None, description="地址")
    date_of_birth: Optional[date] = Field(None, description="出生日期")
    income: Optional[Decimal] = Field(None, description="月收入")
    id_card_number: Optional[str] = Field(None, description="身份证号")
    # id_card_expiry: Optional[date] = Field(None, description="身份证有效期")
    bank_account: Optional[str] = Field(None, description="银行卡号")
    profession: Optional[str] = Field(None, description="职业类别")
    student_verified: Optional[bool] = Field(None, description="学信网认证状态")
    # profile_picture: Optional[str] = Field(None, description="头像URL")

    class Config:
        # orm_mode = True
        from_attributes = True

class CreateUserAuthRequest(BaseModel):
    """
    新增用户认证信息的请求模型
    """
    username: str = Field(..., description="用户名（必须唯一）")
    phone_number: str = Field(..., description="手机号（必须唯一）")
    password: str = Field(..., description="用户密码")
    role: str = Field("user", description="用户权限（默认是 user，可选 admin/root）")

    class Config:
        # orm_mode = True
        from_attributes = True

class CreateUserProfileRequest(BaseModel):
    """
    新增用户个人信息的请求模型
    """
    user_id: int = Field(..., description="用户id")  # 必填
    username: str = Field(..., description="用户名")  # 必填
    full_name: Optional[str] = Field(None, description="姓名")
    phone_number: str = Field(..., description="手机号")  # 必填
    gender: Optional[str] = Field(None, description="性别")
    id_card_number: Optional[str] = Field(None, description="身份证号")
    # id_card_expiry: Optional[date] = Field(None, description="身份证有效期")
    bank_account: Optional[str] = Field(None, description="银行卡号")
    profession: Optional[str] = Field(None, description="职业类别")
    address: Optional[str] = Field(None, description="地址")
    date_of_birth: Optional[date] = Field(None, description="出生年月")
    income: Optional[Decimal] = Field(None, description="月收入")
    student_verified: Optional[bool] = Field(False, description="是否学生认证")  # 默认False
    # profile_picture: Optional[str] = Field(None, description="头像URL")

    class Config:
        # orm_mode = True
        from_attributes = True