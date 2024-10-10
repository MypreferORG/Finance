# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:31 PM
# @Author : Myprefer
# @Des: 贷款相关的schema模型
"""

from pydantic import BaseModel


# 贷款申请请求数据
class LoanApplicationRequest(BaseModel):
    # todo: LoanApplicationRequest 贷款申请请求数据
    pass


# 贷款申请响应数据
class LoanApplicationResponse(BaseModel):
    # todo: LoanApplicationResponse 贷款申请响应数据
    pass


# 贷款状态响应数据
class LoanStatusResponse(BaseModel):
    # todo: LoanStatusResponse 贷款状态响应数据
    pass


# 还款计划响应数据
class RepaymentPlanResponse(BaseModel):
    # todo: RepaymentPlanResponse 还款计划响应数据
    pass


# 还款请求数据
class RepaymentRequest(BaseModel):
    # todo: RepaymentRequest 还款请求数据
    pass
