# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:34 PM
# @Author : Myprefer
# @Des: 贷款业务管理接口
"""
import decimal
import json
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from config import settings
from core.dependences import get_current_user
from models import UserAuth, UserProfile, LoanRecord, InterestRate, RepaymentRecord
from schemas import (LoanApplicationResponse,
                     LoanApplicationRequest,
                     LoanStatusResponse,
                     RepaymentPlanResponse,
                     RepaymentRequest,
                     RepaymentPlan,
                     RepaymentPlanInfo)
from schemas.loan import LoanQuotaResponse
from services.repayment_schedule import generate_repayment_schedule

router = APIRouter()


@router.get("/apply/check", summary="检查贷款额度", response_model=LoanQuotaResponse)
async def check_loan_quota(user: UserAuth = Depends(get_current_user)):
    """
    检查贷款额度逻辑
    :param user: 当前登录用户
    :return: 额度
    """
    # 查询用户
    user_profile = await UserProfile.get_or_none(user=user)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 检查用户个人信息是否完整
    if not user_profile.is_profile_completed:
        raise HTTPException(status_code=400, detail="请先完善个人信息")

    if user_profile.max_amount <= 0 or user_profile.credit <= 0 or user_profile.loaned_amount >= user_profile.max_amount:
        raise HTTPException(status_code=400, detail="额度不足")

    return user_profile


@router.post("/apply/confirm", summary="申请贷款", response_model=LoanApplicationResponse)
async def apply_loan(request: LoanApplicationRequest, user: UserAuth = Depends(get_current_user)):
    """
    贷款申请逻辑
    :param request: 贷款申请请求
    :param user: 当前登录用户
    :return: 贷款记录
    """
    user_profile = await UserProfile.get_or_none(user=user)
    if not user_profile:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 检查借款金额是否有效
    amount = request.amount
    loaned_amount = user_profile.loaned_amount
    if request.amount <= 0 or request.amount >= user_profile.max_amount or amount + loaned_amount > user_profile.max_amount:
        raise HTTPException(status_code=400, detail="借款金额异常")

    # 查询当前利率
    current_interest_rate = await InterestRate.first()
    current_interest_rate = current_interest_rate.interest_rate

    repayment_schedule = generate_repayment_schedule(amount=request.amount,
                                                     loan_term=request.loan_term,
                                                     interest_rate=current_interest_rate,
                                                     repayment_method="等额本息" if request.repayment_method == 1 else "等额本金")

    # todo: 贷款功能具体实现
    # transfer_success = await transfer_loan_to_bank_account(user_profile, request.amount)
    transfer_success = True

    if not transfer_success:
        raise HTTPException(status_code=500, detail="贷款转账失败")

    # 更新用户的已借款金额
    user_profile.loaned_amount += amount
    await user_profile.save()

    # 创建贷款记录
    new_loan = await LoanRecord.create(
        user=user,
        amount=request.amount,
        interest_rate=current_interest_rate,
        loan_term=request.loan_term,
        status="active",
        repayment_method="等额本息" if request.repayment_method == 1 else "等额本金",
        repayment_schedule=repayment_schedule,
        usage=request.usage,
        bank_account=user_profile.bank_account,
    )

    return new_loan


@router.get("/status/{loan_id}", summary="查询贷款状态", response_model=LoanStatusResponse)
async def loan_status(loan_id: int, user: UserAuth = Depends(get_current_user)):
    """
    查询贷款状态逻辑
    :param loan_id: 贷款记录id
    :param user: 当前登录用户
    :return: 贷款记录
    """
    # 根据 loan_id 查询贷款记录
    loan = await LoanRecord.get_or_none(id=loan_id)

    if loan.user_id != user.index and (user.role != 'admin' or user.role != 'root'):
        raise HTTPException(status_code=401, detail="无权查看该记录")

    # 如果找不到贷款记录，抛出 404 错误
    if not loan:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    return loan


@router.get("/repayment-plan/{loan_id}", summary="还款计划", response_model=RepaymentPlanResponse)
async def repayment_plan(loan_id: int, user: UserAuth = Depends(get_current_user)):
    """
    查看还款计划逻辑
    :param loan_id: 贷款记录id
    :param user: 当前登录用户
    :return: 还款计划
    """
    # 根据 loan_id 查询贷款记录
    loan = await LoanRecord.get_or_none(id=loan_id)

    # 如果找不到贷款记录，抛出 404 错误
    if not loan or not loan.repayment_schedule:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    if loan.user_id != user.index and (user.role != 'admin' or user.role != 'root'):
        raise HTTPException(status_code=401, detail="无权查看该记录")

    # 解析还款计划
    repayment_schedule = loan.repayment_schedule

    # 将字符串形式的还款计划解析为列表（假设它是以字符串形式存储的）
    try:
        repayment_schedule_list = json.loads(repayment_schedule)  # 将字符串转换为字典列表
    except (ValueError, SyntaxError):
        raise HTTPException(status_code=500, detail="还款计划格式错误")

    # 生成还款计划的响应数据
    repayment_plan_info = RepaymentPlanInfo(
        loan_id=loan_id,
        amount=loan.amount,
        interest_rate=loan.interest_rate,
        loan_term=loan.loan_term,
        status=loan.status,
        repayment_method=loan.repayment_method,
        bank_account=loan.bank_account,
        created_at=loan.created_at
    )

    repayment_plan_response = RepaymentPlanResponse(
        loan_record=repayment_plan_info,
        repayment_plan=[
            RepaymentPlan(
                installment_number=item['installment_number'],
                amount_due=item['amount_due'],
                due_date=item['due_date']
            ) for item in repayment_schedule_list
        ]
    )

    return repayment_plan_response


@router.post("/repayment", summary="还款", response_model=RepaymentRequest)
async def repayment(request: RepaymentRequest, user: UserAuth = Depends(get_current_user)):
    """
    还款逻辑
    :param request: 还款请求
    :param user: 当前登录用户
    :return: 还款记录
    """
    # 查询用户
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 查询贷款记录
    loan_record = await LoanRecord.get_or_none(id=request.loan_id, user=user)

    # 如果找不到贷款记录，抛出404错误
    if not loan_record:
        raise HTTPException(status_code=404, detail="贷款记录未找到")

    if loan_record.user_id != user.index and (user.role != 'admin' or user.role != 'root'):
        raise HTTPException(status_code=401, detail="用户错误")

    # 验证还款金额
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="还款金额必须大于0")

    # 检查用户的还款金额是否符合当前应还款金额
    if loan_record.repayment_amount + request.amount > loan_record.amount:
        raise HTTPException(status_code=400, detail="还款金额超过贷款金额")

    # todo: 实际的还款逻辑
    # payment_url = generate_payment_url(
    #     order_id=f"repayment-{loan_record.id}",
    #     total_amount=Decimal(request.amount),
    #     subject="贷款还款",
    #     return_url=settings.ALIPAY_SETTING.get("RETURN_URL")
    # )
    payment_url = "http://localhost:8000"

    # 更新贷款记录的已还款金额
    loan_record.repayment_amount += Decimal(request.amount)
    if loan_record.repayment_amount >= loan_record.amount:
        loan_record.status = "completed"  # 完成还款，更新状态
    await loan_record.save()

    # 更新用户的已借款金额
    user_profile = await UserProfile.get_or_none(user=user)
    user_profile.loaned_amount -= Decimal(request.amount)
    await user_profile.save()

    # 创建还款记录
    await RepaymentRecord.create(
        loan=loan_record,
        user=user,
        amount=Decimal(request.amount),
        status="successful",  # 假设还款成功
        message="还款成功"
    )

    # 返回支付链接给用户
    return {"payment_url": payment_url}


@router.get("/set-rate/{rate}", summary="设置贷款利率")
async def set_rate(rate: decimal.Decimal, user: UserAuth = Depends(get_current_user)):
    """
    设置贷款利率
    :param rate: 利率
    :param user: 当前登录用户
    :return: 设置结果
    """
    # 验证用户角色是否为 admin
    if user.role != "admin" and user.role != "root":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )

    await InterestRate.update_or_create(interest_rate=rate)

    return {
        "status": "success",
        "rate": rate
    }


@router.get("/quota", summary="查询借款额度")
async def get_loan_quota(user: UserAuth = Depends(get_current_user)):
    """
    查询借款额度逻辑
    :param user: 当前登录用户
    :return: 额度
    """
    user_profile = await UserProfile.get_or_none(user=user)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="用户未找到")

    return {"quota": user_profile.max_amount}


@router.get("/list/{status}",
            summary="查询不同状态的借款列表",
            response_model=List[LoanStatusResponse])
async def loan_status(status: str, user: UserAuth = Depends(get_current_user)):
    """
    查询借款列表状态逻辑
    :param status: 贷款状态
    :param user: 当前登录用户
    :return: 贷款记录列表
    """
    # 检查用户是否存在
    if user is None:
        raise HTTPException(status_code=404, detail="用户未找到")

    # 根据不同状态查询用户的贷款记录
    if status not in ["active", "completed", "overdue", "defaulted"]:
        raise HTTPException(status_code=400, detail="无效的贷款状态")

    # 查询贷款记录
    loans = await LoanRecord.filter(user=user, status=status).order_by("-created_at")

    return loans
