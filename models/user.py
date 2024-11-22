# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:48 PM
# @Author : Myprefer
# @Des: 用户模型
"""
from datetime import date

from tortoise import fields
from tortoise.models import Model


class UserAuth(Model):
    """
    用户注册信息表：用于登录和找回密码
    """
    index = fields.IntField(pk=True, description="索引")
    id = fields.CharField(max_length=32, unique=True, description='唯一用户id')
    username = fields.CharField(max_length=50, unique=True, description='唯一用户名, 用于登录')
    phone_number = fields.CharField(max_length=11, unique=True, description='唯一用户电话号码, 用于登录及找回密码')
    hashed_password = fields.CharField(max_length=255, description='加密后的密码')
    role = fields.CharField(max_length=10, default="user", description="用户权限, 分为 user/admin/root")
    created_at = fields.DatetimeField(auto_now_add=True, description="注册时间")
    updated_at = fields.DatetimeField(auto_now=True, description="信息更新时间")

    class Meta:
        table_name = 'user_auth'
        indexes = [('username', 'phone_number')]  # 创建索引

    def __str__(self):
        return f"UserAuth(id={self.id}, username={self.username})"


class UserSignLog(Model):
    """
    用户登录日志表：记录用户的登录、登出操作
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("finance.UserAuth", related_name="user_login_logs", description="关联的用户")
    action = fields.CharField(max_length=50, description="用户操作类型, 登录/登出")
    ip_address = fields.CharField(max_length=45, null=True, description="IP地址（IPv4或IPv6）")
    user_agent = fields.CharField(max_length=255, null=True, description="用户设备信息（浏览器、操作系统等）")
    success = fields.BooleanField(default=True, description="操作是否成功")
    message = fields.TextField(null=True, description="额外的操作结果信息或错误消息")
    created_at = fields.DatetimeField(auto_now_add=True, description="操作发生的时间")

    class Meta:
        table = "user_login_log"
        indexes = [("user", "action")]  # 根据用户和操作类型创建索引

    def __str__(self):
        return f"UserLoginLog(user={self.user.username}, action={self.action}, success={self.success})"


class UserProfile(Model):
    """
    用户基本个人信息表
    """
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("finance.UserAuth", related_name="user_profiles", description="关联的用户账户")
    username = fields.CharField(max_length=50, unique=True, description='唯一用户名')
    full_name = fields.CharField(max_length=100, null=True, description="姓名")
    phone_number = fields.CharField(max_length=20, description="电话号码")
    gender = fields.CharField(max_length=10, null=True, description="性别")
    id_card_number = fields.CharField(max_length=18, null=True, unique=True, description="身份证号")
    id_card_expiry = fields.DateField(null=True, description="身份证有效期")
    bank_account = fields.CharField(max_length=50, null=True, description="银行卡号")
    profession = fields.CharField(max_length=50, null=True, description="职业类别")
    address = fields.TextField(null=True, description="住址")
    date_of_birth = fields.DateField(null=True, description="出生年月")
    student_verified = fields.BooleanField(default=False, description="学信网认证，学生专属")
    profile_picture = fields.CharField(max_length=255, null=True, description="头像URL")
    income = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="月收入")
    max_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0.0, description="最大借款额度")
    credit = fields.DecimalField(max_digits=10, decimal_places=2, default=0.0, description="信用分数")
    loaned_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0.0, description="已经贷款金额")
    is_profile_completed = fields.BooleanField(default=False, description="是否已经完善个人信息")

    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_profile"
        indexes = [("user",)]  # 根据用户创建索引


class UserApplication(Model):
    """
    A卡评分卡所需信息
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("finance.UserAuth", related_name="user_applications", description="关联的用户")
    real_name_verified = fields.BooleanField(default=False, description="用户实名制是否通过核实")
    age = fields.IntField(null=True, description="用户年龄")
    is_student = fields.BooleanField(default=False, description="是否大学生客户")
    is_blacklisted = fields.BooleanField(default=False, description="是否黑名单客户")
    is_unhealthy_4g_user = fields.BooleanField(default=False, description="是否4G不健康客户")
    network_age_months = fields.IntField(null=True, description="用户网龄（月）")
    last_payment_months_ago = fields.IntField(null=True, description="用户最近一次缴费距今时长（月）")
    last_payment_amount = fields.FloatField(null=True, description="最近一次缴费金额（元）")
    avg_monthly_spending_6_months = fields.FloatField(null=True, description="用户近6个月平均消费值（元）")
    current_bill_total = fields.FloatField(null=True, description="用户账单当月总费用（元）")
    current_account_balance = fields.FloatField(null=True, description="用户当月账户余额（元）")
    has_outstanding_payment = fields.BooleanField(default=False, description="当前是否欠费缴费")
    call_fee_sensitivity = fields.IntField(null=True, description="用户话费敏感度")
    contacts_this_month = fields.IntField(null=True, description="当月通话交往圈人数")
    is_frequent_mall_visitor = fields.BooleanField(default=False, description="是否经常逛商场的人")
    avg_mall_visits_3_months = fields.IntField(null=True, description="近三个月月均商场出现次数")
    visited_fuzhou_cangshan_wanda = fields.BooleanField(default=False, description="当月是否逛过福州仓山万达")
    visited_fuzhou_sam_club = fields.BooleanField(default=False, description="当月是否到过福州山姆会员店")
    watched_movie = fields.BooleanField(default=False, description="当月是否看电影")
    visited_scenic_spot = fields.BooleanField(default=False, description="当月是否景点游览")
    used_sports_facility = fields.BooleanField(default=False, description="当月是否体育场馆消费")
    online_shopping_app_usage = fields.IntField(null=True, description="当月网购类应用使用次数")
    logistics_app_usage = fields.IntField(null=True, description="当月物流快递类应用使用次数")
    finance_app_usage = fields.IntField(null=True, description="当月金融理财类应用使用总次数")
    video_app_usage = fields.IntField(null=True, description="当月视频播放类应用使用次数")
    airplane_app_usage = fields.IntField(null=True, description="当月飞机类应用使用次数")
    train_app_usage = fields.IntField(null=True, description="当月火车类应用使用次数")
    travel_info_app_usage = fields.IntField(null=True, description="当月旅游资讯类应用使用次数")
    credit_score = fields.FloatField(null=True, description="用户信用分")
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_application"
        indexes = [("user",)]  # 针对用户编码创建索引


class UserBehavior(Model):
    """
    B卡评分卡所需信息
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("finance.UserAuth", related_name="user_behaviors", description="关联的用户")
    age = fields.IntField(null=True, description="用户年龄")
    bank_cards_count = fields.IntField(null=True, description="全国股份制商业银行卡片数")
    remote_transaction_months = fields.IntField(null=True, description="近6个月有异地交易的月份数")
    internet_transaction_avg = fields.FloatField(null=True, description="近6个月互联网交易笔数均值")
    financial_transaction_months = fields.IntField(null=True, description="近6个月有金融类交易的月份数")
    financial_transaction_avg_amount = fields.FloatField(null=True, description="近6个月金融类交易额均值")
    max_loan_amount_180_days = fields.FloatField(null=True, description="180天内单笔放款金额最大值")
    min_loan_amount_180_days = fields.FloatField(null=True, description="180天内单笔放款金额最小值")
    apply_loan_company_number = fields.IntField(null=True, description="申请贷款机构数")
    created_at = fields.DatetimeField(auto_now_add=True, description="记录创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="记录更新时间")

    class Meta:
        table = "user_behavior"
        indexes = [("user",)]
