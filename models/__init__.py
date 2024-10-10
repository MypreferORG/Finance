# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:50 PM
# @Author : Myprefer
# @Des: 数据库模型定义
"""

from .article import Article, Announcement
from .user import UserAuth, UserSignLog, UserApplication, UserBehavior
from .loan import LoanRecord, RepaymentRecord

__all__ = ["Article", "Announcement", "UserAuth",
           "UserSignLog", "UserApplication", "UserBehavior",
           "LoanRecord", "RepaymentRecord"]
