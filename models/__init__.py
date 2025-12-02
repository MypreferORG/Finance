# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:50 PM
# @Author : Myprefer
# @Des: 数据库模型定义
"""

from .article import Article, Announcement
from .user import UserAuth, UserSignLog, UserApplication, UserBehavior, UserProfile
from .loan import LoanRecord, RepaymentRecord, InterestRate
from .model import AIModel
from .review import ReviewApplication
from .decision import DecisionRule, DecisionExecution, DecisionTestCase, DecisionStatistics
from .app_blacklist import AppBlacklist
from .call_blacklist import CallBlacklist
from .user_device_data import (
    UserSmsRecord, UserAppRecord, UserContactRecord, 
    UserImageRecord, UserDeviceDataBatch
)

__all__ = ["Article", "Announcement", "UserAuth",
           "UserSignLog", "UserApplication", "UserBehavior", "UserProfile",
           "LoanRecord", "RepaymentRecord", "InterestRate", "AIModel", "ReviewApplication",
           "DecisionRule", "DecisionExecution", "DecisionTestCase", "DecisionStatistics",
           "AppBlacklist", "CallBlacklist",
           "UserSmsRecord", "UserAppRecord", "UserContactRecord",
           "UserImageRecord", "UserDeviceDataBatch"]

