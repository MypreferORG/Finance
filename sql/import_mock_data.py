# -*- coding: utf-8 -*-
"""
# @Create on : 2024/07/11
# @Author : AI Assistant
# @Des: 导入模拟数据到数据库
"""

import asyncio
import json
import datetime
from decimal import Decimal

from tortoise import Tortoise

from Finance.models.mock_data import generate_all_mock_data
from Finance.models import (
    UserAuth, UserProfile, UserApplication, UserBehavior, UserSignLog,
    LoanRecord, RepaymentRecord, InterestRate,
    Article, Announcement,
    AIModel,
    ReviewApplication
)


async def init_tortoise():
    """初始化Tortoise ORM"""
    await Tortoise.init(
        # 使用mysql数据库
        db_url="mysql://finance1:79sdiubfhsiojeio3@localhost:3306/finance",
        modules={'finance': ['__main__']}
    )
    await Tortoise.generate_schemas()


async def import_user_data(mock_data):
    """导入用户相关数据"""
    print("正在导入用户数据...")
    
    # 导入用户认证数据
    user_map = {}  # 用于存储用户ID映射
    for user_data in mock_data["users"]:
        user = await UserAuth.create(
            index=user_data["index"],
            id=user_data["id"],
            username=user_data["username"],
            phone_number=user_data["phone_number"],
            hashed_password=user_data["hashed_password"],
            role=user_data["role"],
            created_at=datetime.datetime.fromisoformat(user_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(user_data["updated_at"])
        )
        user_map[user_data["index"]] = user
    
    # 导入用户个人资料
    for profile_data in mock_data["profiles"]:
        user = user_map.get(profile_data["user_id"])
        if not user:
            continue
            
        await UserProfile.create(
            user=user,
            username=profile_data["username"],
            full_name=profile_data["full_name"],
            phone_number=profile_data["phone_number"],
            gender=profile_data["gender"],
            id_card_number=profile_data["id_card_number"],
            id_card_expiry=profile_data["id_card_expiry"] and datetime.date.fromisoformat(profile_data["id_card_expiry"]),
            bank_account=profile_data["bank_account"],
            profession=profile_data["profession"],
            address=profile_data["address"],
            date_of_birth=profile_data["date_of_birth"] and datetime.date.fromisoformat(profile_data["date_of_birth"]),
            student_verified=profile_data["student_verified"],
            profile_picture=profile_data["profile_picture"],
            income=profile_data["income"] and Decimal(profile_data["income"]),
            max_amount=Decimal(profile_data["max_amount"]),
            credit=Decimal(profile_data["credit"]),
            loaned_amount=Decimal(profile_data["loaned_amount"]),
            is_profile_completed=profile_data["is_profile_completed"],
            created_at=datetime.datetime.fromisoformat(profile_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(profile_data["updated_at"])
        )
    
    # 导入用户A卡评分卡数据
    for app_data in mock_data["applications"]:
        user = user_map.get(app_data["user_id"])
        if not user:
            continue
            
        await UserApplication.create(
            user=user,
            real_name_verified=app_data["real_name_verified"],
            age=app_data["age"],
            is_student=app_data["is_student"],
            is_blacklisted=app_data["is_blacklisted"],
            is_unhealthy_4g_user=app_data["is_unhealthy_4g_user"],
            network_age_months=app_data["network_age_months"],
            last_payment_months_ago=app_data["last_payment_months_ago"],
            last_payment_amount=app_data["last_payment_amount"],
            avg_monthly_spending_6_months=app_data["avg_monthly_spending_6_months"],
            current_bill_total=app_data["current_bill_total"],
            current_account_balance=app_data["current_account_balance"],
            has_outstanding_payment=app_data["has_outstanding_payment"],
            call_fee_sensitivity=app_data["call_fee_sensitivity"],
            contacts_this_month=app_data["contacts_this_month"],
            is_frequent_mall_visitor=app_data["is_frequent_mall_visitor"],
            avg_mall_visits_3_months=app_data["avg_mall_visits_3_months"],
            visited_fuzhou_cangshan_wanda=app_data["visited_fuzhou_cangshan_wanda"],
            visited_fuzhou_sam_club=app_data["visited_fuzhou_sam_club"],
            watched_movie=app_data["watched_movie"],
            visited_scenic_spot=app_data["visited_scenic_spot"],
            used_sports_facility=app_data["used_sports_facility"],
            online_shopping_app_usage=app_data["online_shopping_app_usage"],
            logistics_app_usage=app_data["logistics_app_usage"],
            finance_app_usage=app_data["finance_app_usage"],
            video_app_usage=app_data["video_app_usage"],
            airplane_app_usage=app_data["airplane_app_usage"],
            train_app_usage=app_data["train_app_usage"],
            travel_info_app_usage=app_data["travel_info_app_usage"],
            credit_score=app_data["credit_score"],
            created_at=datetime.datetime.fromisoformat(app_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(app_data["updated_at"])
        )
    
    # 导入用户B卡评分卡数据
    for behavior_data in mock_data["behaviors"]:
        user = user_map.get(behavior_data["user_id"])
        if not user:
            continue
            
        await UserBehavior.create(
            user=user,
            age=behavior_data["age"],
            bank_cards_count=behavior_data["bank_cards_count"],
            remote_transaction_months=behavior_data["remote_transaction_months"],
            internet_transaction_avg=behavior_data["internet_transaction_avg"],
            financial_transaction_months=behavior_data["financial_transaction_months"],
            financial_transaction_avg_amount=behavior_data["financial_transaction_avg_amount"],
            max_loan_amount_180_days=behavior_data["max_loan_amount_180_days"],
            min_loan_amount_180_days=behavior_data["min_loan_amount_180_days"],
            apply_loan_company_number=behavior_data["apply_loan_company_number"],
            created_at=datetime.datetime.fromisoformat(behavior_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(behavior_data["updated_at"])
        )
    
    # 导入用户登录日志
    for log_data in mock_data["sign_logs"]:
        user = user_map.get(log_data["user_id"])
        if not user:
            continue
            
        await UserSignLog.create(
            user=user,
            action=log_data["action"],
            ip_address=log_data["ip_address"],
            user_agent=log_data["user_agent"],
            success=log_data["success"],
            message=log_data["message"],
            created_at=datetime.datetime.fromisoformat(log_data["created_at"])
        )
    
    return user_map


async def import_article_data(mock_data):
    """导入文章和公告数据"""
    print("正在导入文章和公告数据...")
    
    # 导入文章数据
    article_map = {}
    for article_data in mock_data["articles"]:
        article = await Article.create(
            link=article_data["link"],
            title=article_data["title"],
            publish_date=datetime.datetime.fromisoformat(article_data["publish_date"]),
            summary=article_data["summary"]
        )
        article_map[article_data["id"]] = article
    
    # 导入公告数据
    for announcement_data in mock_data["announcements"]:
        await Announcement.create(
            title=announcement_data["title"],
            content=announcement_data["content"],
            publish_date=datetime.datetime.fromisoformat(announcement_data["publish_date"]),
            updated_at=datetime.datetime.fromisoformat(announcement_data["updated_at"]),
            status=announcement_data["status"],
            author=announcement_data["author"],
            expiration_date=announcement_data["expiration_date"] and datetime.datetime.fromisoformat(announcement_data["expiration_date"])
        )
    
    return article_map


async def import_loan_data(mock_data, user_map):
    """导入贷款相关数据"""
    print("正在导入贷款数据...")
    
    # 导入贷款记录
    loan_map = {}
    for loan_data in mock_data["loan_records"]:
        user = user_map.get(loan_data["user_id"])
        if not user:
            continue
            
        loan = await LoanRecord.create(
            user=user,
            amount=Decimal(loan_data["amount"]),
            interest_rate=Decimal(loan_data["interest_rate"]),
            loan_term=loan_data["loan_term"],
            status=loan_data["status"],
            repayment_method=loan_data["repayment_method"],
            repayment_amount=Decimal(loan_data["repayment_amount"]),
            repayment_schedule=loan_data["repayment_schedule"],
            usage=loan_data["usage"],
            bank_account=loan_data["bank_account"],
            income=loan_data["income"] and Decimal(loan_data["income"]),
            credit_score=loan_data["credit_score"],
            auditor=loan_data["auditor"],
            audit_time=loan_data["audit_time"] and datetime.datetime.fromisoformat(loan_data["audit_time"]),
            remark=loan_data["remark"],
            created_at=datetime.datetime.fromisoformat(loan_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(loan_data["updated_at"])
        )
        loan_map[loan_data["id"]] = loan
    
    # 导入还款记录
    for repayment_data in mock_data["repayment_records"]:
        user = user_map.get(repayment_data["user_id"])
        loan = loan_map.get(repayment_data["loan_id"])
        if not user or not loan:
            continue
            
        await RepaymentRecord.create(
            loan=loan,
            user=user,
            amount=Decimal(repayment_data["amount"]),
            repayment_date=datetime.datetime.fromisoformat(repayment_data["repayment_date"]),
            status=repayment_data["status"],
            message=repayment_data["message"]
        )
    
    # 导入利率数据
    for rate_data in mock_data["interest_rates"]:
        await InterestRate.create(
            interest_rate=Decimal(rate_data["interest_rate"])
        )
    
    return loan_map


async def import_model_data(mock_data):
    """导入AI模型数据"""
    print("正在导入AI模型数据...")
    
    for model_data in mock_data["ai_models"]:
        await AIModel.create(
            name=model_data["name"],
            version=model_data["version"],
            file_path=model_data["file_path"],
            description=model_data["description"],
            technical_details=model_data["technical_details"],
            file_size=model_data["file_size"],
            file_extension=model_data["file_extension"],
            status=model_data["status"],
            ks_value=model_data["ks_value"],
            bad_rate=model_data["bad_rate"],
            accuracy=model_data["accuracy"],
            recall=model_data["recall"],
            precision=model_data["precision"],
            created_at=datetime.datetime.fromisoformat(model_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(model_data["updated_at"])
        )


async def import_review_data(mock_data):
    """导入复审申请数据"""
    print("正在导入复审申请数据...")
    
    for review_data in mock_data["review_applications"]:
        await ReviewApplication.create(
            original_audit_id=review_data["original_audit_id"],
            applicant_name=review_data["applicant_name"],
            phone=review_data["phone"],
            id_card=review_data["id_card"],
            loan_amount=Decimal(review_data["loan_amount"]),
            loan_purpose=review_data["loan_purpose"],
            original_result=review_data["original_result"],
            original_reason=review_data["original_reason"],
            original_auditor=review_data["original_auditor"],
            original_audit_time=review_data["original_audit_time"] and datetime.datetime.fromisoformat(review_data["original_audit_time"]),
            review_reason=review_data["review_reason"],
            review_apply_time=datetime.datetime.fromisoformat(review_data["review_apply_time"]),
            status=review_data["status"],
            priority=review_data["priority"],
            additional_docs=json.loads(review_data["additional_docs"]),
            review_auditor=review_data["review_auditor"],
            review_time=review_data["review_time"] and datetime.datetime.fromisoformat(review_data["review_time"]),
            review_result=review_data["review_result"],
            review_comment=review_data["review_comment"],
            created_at=datetime.datetime.fromisoformat(review_data["created_at"]),
            updated_at=datetime.datetime.fromisoformat(review_data["updated_at"])
        )


async def import_all_data():
    """导入所有模拟数据"""
    print("开始导入模拟数据...")
    
    # 生成模拟数据
    mock_data = generate_all_mock_data()
    
    # 初始化数据库连接
    await init_tortoise()
    
    try:
        # 导入各类数据
        user_map = await import_user_data(mock_data)
        article_map = await import_article_data(mock_data)
        loan_map = await import_loan_data(mock_data, user_map)
        await import_model_data(mock_data)
        await import_review_data(mock_data)
        
        # 建立用户和文章的多对多关系
        # 随机为用户推荐一些文章
        import random
        for user in user_map.values():
            # 为每个用户随机推荐1-5篇文章
            article_ids = random.sample(list(article_map.keys()), random.randint(1, min(5, len(article_map))))
            for article_id in article_ids:
                await user.recommended_articles.add(article_map[article_id])
        
        print("模拟数据导入完成！")
    except Exception as e:
        print(f"导入数据时出错: {e}")
    finally:
        # 关闭数据库连接
        await Tortoise.close_connections()


if __name__ == "__main__":
    # 运行导入脚本
    asyncio.run(import_all_data())