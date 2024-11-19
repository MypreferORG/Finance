# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/16 19:59
# @Author : Myprefer
# @Des: 生成还款计划
"""
import json
from datetime import datetime, timedelta
from decimal import Decimal
from models import LoanRecord


def generate_repayment_schedule(amount: Decimal, loan_term: int, interest_rate: Decimal, repayment_method: str):
    """
    生成还款计划
    :param amount: 贷款金额
    :param loan_term: 贷款期限（月）
    :param interest_rate: 年利率
    :param repayment_method: 还款方式 (等额本金/等额本息)
    :return: 还款计划的字符串表示（可以存储到数据库）
    """
    repayment_schedule = []
    monthly_interest_rate = interest_rate / 12  # 月利率
    loan_amount = Decimal(amount)

    if repayment_method == "等额本金":
        # 等额本金计算
        monthly_principal = loan_amount / loan_term
        for i in range(1, loan_term + 1):
            # 每期利息=剩余本金*月利率
            monthly_interest = (loan_amount - (i - 1) * monthly_principal) * monthly_interest_rate
            total_payment = monthly_principal + monthly_interest
            due_date = datetime.utcnow() + timedelta(days=30 * i)  # 生成预计还款日期
            repayment_schedule.append({
                "installment_number": i,
                "amount_due": round(float(total_payment), 2),
                "due_date": due_date.strftime('%Y-%m-%d')  # 格式化日期为字符串
            })
    elif repayment_method == "等额本息":
        # 等额本息计算
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term) / (
                (1 + monthly_interest_rate) ** loan_term - 1)
        for i in range(1, loan_term + 1):
            due_date = datetime.utcnow() + timedelta(days=30 * i)  # 生成预计还款日期
            repayment_schedule.append({
                "installment_number": i,
                "amount_due": round(float(monthly_payment), 2),
                "due_date": due_date.strftime('%Y-%m-%d')  # 格式化日期为字符串
            })
    else:
        raise ValueError("不支持的还款方式")

    return json.dumps(repayment_schedule)

