# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:30 PM
# @Author : Myprefer
# @Des: 贷款模型
"""

from tortoise import fields
from tortoise.models import Model


class LoanRecord(Model):
    """
    贷款记录表：用于记录所有用户的借款信息
    """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("finance.UserAuth", related_name="loan_records", description="关联的用户")
    amount = fields.DecimalField(max_digits=10, decimal_places=2, description="借款金额")
    interest_rate = fields.DecimalField(max_digits=5, decimal_places=2, description="年利率")
    loan_term = fields.IntField(description="贷款期限（以月为单位）")
    status = fields.CharField(max_length=20, default="active", description="贷款状态（如：active、completed、defaulted等）")
    repayment_amount = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00, description="已还款金额")
    repayment_schedule = fields.TextField(description="还款计划（如每期还款金额、还款日期等）")
    created_at = fields.DatetimeField(auto_now_add=True, description="贷款申请时间")
    updated_at = fields.DatetimeField(auto_now=True, description="贷款信息更新时间")

    class Meta:
        table = "loan_record"
        indexes = [("user", "created_at")]  # 根据用户和贷款申请时间创建索引

    def __str__(self):
        return f"LoanRecord(id={self.id}, user={self.user.username}, amount={self.amount}, status={self.status})"


class RepaymentRecord(Model):
    """
    还款记录表：用于记录所有用户的还款信息
    """
    id = fields.IntField(pk=True)
    loan = fields.ForeignKeyField("finance.LoanRecord", related_name="repayment_records", description="关联的贷款记录")
    user = fields.ForeignKeyField("finance.UserAuth", related_name="repayment_records", description="关联的用户")
    amount = fields.DecimalField(max_digits=10, decimal_places=2, description="还款金额")
    repayment_date = fields.DatetimeField(auto_now_add=True, description="还款时间")
    status = fields.CharField(max_length=20, default="successful",
                              description="还款状态（如：successful、failed、overdue等）")
    message = fields.TextField(null=True, description="还款结果的附加信息（如失败原因等）")

    class Meta:
        table = "repayment_record"
        indexes = [("loan", "repayment_date")]  # 根据贷款记录和还款时间创建索引

    def __str__(self):
        return f"RepaymentRecord(id={self.id}, loan_id={self.loan.id}, user={self.user.username}, amount={self.amount}, status={self.status})"