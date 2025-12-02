# -*- coding: utf-8 -*-
"""
# @Create on : 2025/12/02
# @Author : Copilot
# @Des: 用户设备数据模型（短信、应用列表、通讯录、图片）
"""
from tortoise import fields
from tortoise.models import Model


class UserSmsRecord(Model):
    """用户短信记录表"""
    id = fields.IntField(pk=True, description="主键ID")
    user = fields.ForeignKeyField("finance.UserAuth", related_name="sms_records", description="关联的用户")
    telphone = fields.CharField(max_length=50, null=True, description="发送者号码")
    content = fields.TextField(description="短信内容")
    send_date = fields.DatetimeField(null=True, description="短信发送时间")
    sms_type = fields.CharField(max_length=20, default="received", description="短信类型: received/sent")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_sms_record"
        indexes = [("user",), ("telphone",)]

    def __str__(self):
        return f"UserSmsRecord(user={self.user_id}, telphone={self.telphone})"


class UserAppRecord(Model):
    """用户应用列表记录表"""
    id = fields.IntField(pk=True, description="主键ID")
    user = fields.ForeignKeyField("finance.UserAuth", related_name="app_records", description="关联的用户")
    name = fields.CharField(max_length=200, description="应用名称")
    pkg_name = fields.CharField(max_length=200, null=True, description="包名")
    version_name = fields.CharField(max_length=50, null=True, description="版本名")
    version_code = fields.IntField(null=True, description="版本号")
    is_system_app = fields.BooleanField(default=False, description="是否系统应用")
    install_time = fields.DatetimeField(null=True, description="安装时间")
    last_update_time = fields.DatetimeField(null=True, description="最后更新时间")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_app_record"
        indexes = [("user",), ("name",), ("pkg_name",)]

    def __str__(self):
        return f"UserAppRecord(user={self.user_id}, name={self.name})"


class UserContactRecord(Model):
    """用户通讯录记录表"""
    id = fields.IntField(pk=True, description="主键ID")
    user = fields.ForeignKeyField("finance.UserAuth", related_name="contact_records", description="关联的用户")
    display_name = fields.CharField(max_length=100, null=True, description="联系人姓名")
    phone_number = fields.CharField(max_length=50, description="电话号码(归一化后)")
    phone_number_raw = fields.CharField(max_length=50, null=True, description="原始电话号码")
    phone_type = fields.CharField(max_length=20, null=True, description="号码类型: mobile/home/work等")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_contact_record"
        indexes = [("user",), ("phone_number",)]

    def __str__(self):
        return f"UserContactRecord(user={self.user_id}, name={self.display_name})"


class UserImageRecord(Model):
    """用户图片记录表（身份证、人脸等）"""
    id = fields.IntField(pk=True, description="主键ID")
    user = fields.ForeignKeyField("finance.UserAuth", related_name="image_records", description="关联的用户")
    image_type = fields.CharField(max_length=50, description="图片类型: id_card_front/id_card_back/face/other")
    image_url = fields.CharField(max_length=500, null=True, description="图片URL或路径")
    image_data = fields.TextField(null=True, description="图片Base64数据(可选)")
    ocr_result = fields.JSONField(null=True, description="OCR识别结果")
    verify_status = fields.CharField(max_length=20, default="pending", description="验证状态: pending/passed/failed")
    verify_message = fields.TextField(null=True, description="验证消息")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_image_record"
        indexes = [("user",), ("image_type",)]

    def __str__(self):
        return f"UserImageRecord(user={self.user_id}, type={self.image_type})"


class UserDeviceDataBatch(Model):
    """用户设备数据批量上传记录表（用于追踪上传批次）"""
    id = fields.IntField(pk=True, description="主键ID")
    user = fields.ForeignKeyField("finance.UserAuth", related_name="device_data_batches", description="关联的用户")
    batch_id = fields.CharField(max_length=64, unique=True, description="批次ID")
    data_type = fields.CharField(max_length=20, description="数据类型: sms/app/contact/image/all")
    total_count = fields.IntField(default=0, description="数据总条数")
    success_count = fields.IntField(default=0, description="成功导入条数")
    failed_count = fields.IntField(default=0, description="失败条数")
    status = fields.CharField(max_length=20, default="processing", description="状态: processing/completed/failed")
    error_message = fields.TextField(null=True, description="错误信息")
    
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_device_data_batch"
        indexes = [("user",), ("batch_id",), ("data_type",)]

    def __str__(self):
        return f"UserDeviceDataBatch(user={self.user_id}, batch={self.batch_id})"
