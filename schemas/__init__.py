# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 8:50 PM
# @Author : Myprefer
# @Des: schema模型
"""

from .article import (
    CreateArticleRequest,
    ArticleResponse,
    ArticleAbstractResponse,
    CreateAnnouncementRequest,
    AnnouncementResponse,
    UpdateAnnouncementRequest,
    AnnouncementAbstractResponse
)

from .auth import (
    RegisterRequest,
    RegisterResponse,
    LoginWithPasswordRequest,
    LoginWithVerificationCodeRequest,
    LoginResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from .loan import (
    LoanStatusResponse,
    LoanApplicationRequest,
    LoanApplicationResponse,
    RepaymentPlanResponse,
    RepaymentRequest,
    RepaymentPlanInfo,
    RepaymentResponse,
    RepaymentPlan
)

from .notification import (
    NotificationResponse,
    LoanNotificationsResponse
)

from .support import (
    SupportRequest,
    SupportResponse,
)

from .user import (
    UserProfileResponse,
    UpdateProfileRequest,
    VerifyAcademicRequest,
    VerifyIdentityRequest
)
