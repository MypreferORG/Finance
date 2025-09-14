# -*- coding: utf-8 -*-
"""
# @Create on : 2024/07/11
# @Author : AI Assistant
# @Des: 模拟数据生成脚本
"""

import json
import random
import datetime
import hashlib
import uuid
from decimal import Decimal
from typing import List, Dict, Any, Optional

# 固定随机种子以确保可重复性
random.seed(42)

# 辅助函数
def generate_id() -> str:
    """生成唯一ID"""
    return uuid.uuid4().hex

def hash_password(password: str) -> str:
    """简单的密码哈希"""
    return hashlib.sha256(password.encode()).hexdigest()

def random_date(start_date: datetime.datetime, end_date: datetime.datetime) -> datetime.datetime:
    """生成两个日期之间的随机日期"""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)

def random_datetime(start_date: datetime.datetime, end_date: datetime.datetime) -> datetime.datetime:
    """生成两个日期之间的随机日期时间"""
    time_between_dates = end_date - start_date
    seconds_between_dates = time_between_dates.total_seconds()
    random_seconds = random.randrange(int(seconds_between_dates))
    return start_date + datetime.timedelta(seconds=random_seconds)

def generate_phone_number() -> str:
    """生成随机手机号"""
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    return random.choice(prefixes) + ''.join(random.choice('0123456789') for _ in range(8))

def generate_id_card() -> str:
    """生成随机身份证号"""
    # 简化版，实际身份证有更复杂的规则
    return ''.join(random.choice('0123456789') for _ in range(18))

def generate_bank_account() -> str:
    """生成随机银行卡号"""
    return ''.join(random.choice('0123456789') for _ in range(16))

# 模拟数据生成
def generate_user_auth_data(count: int = 10) -> List[Dict[str, Any]]:
    """生成用户认证数据"""
    roles = ["user", "admin", "root"]
    role_weights = [0.8, 0.15, 0.05]  # 80% 普通用户, 15% 管理员, 5% 超级管理员
    
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2024, 7, 1)
    
    users = []
    for i in range(1, count + 1):
        user_id = generate_id()
        username = f"user_{i}"
        phone_number = generate_phone_number()
        role = random.choices(roles, weights=role_weights)[0]
        created_at = random_datetime(start_date, end_date)
        updated_at = random_datetime(created_at, end_date)
        
        users.append({
            "index": i,
            "id": user_id,
            "username": username,
            "phone_number": phone_number,
            "hashed_password": hash_password(f"password_{i}"),
            "role": role,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        })
    
    return users

def generate_user_profile_data(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """生成用户个人资料数据"""
    genders = ["男", "女"]
    professions = ["学生", "教师", "工程师", "医生", "律师", "销售", "自由职业", "其他"]
    addresses = ["北京市海淀区", "上海市浦东新区", "广州市天河区", "深圳市南山区", "杭州市西湖区", "成都市武侯区"]
    
    profiles = []
    for i, user in enumerate(users, 1):
        # 70%的用户有完整资料
        is_complete = random.random() < 0.7
        
        gender = random.choice(genders) if is_complete else None
        full_name = f"用户{i}" if is_complete else None
        id_card_number = generate_id_card() if is_complete else None
        id_card_expiry = (datetime.datetime.now() + datetime.timedelta(days=random.randint(365, 3650))).date() if is_complete else None
        bank_account = generate_bank_account() if is_complete else None
        profession = random.choice(professions) if is_complete else None
        address = random.choice(addresses) if is_complete else None
        date_of_birth = (datetime.datetime.now() - datetime.timedelta(days=random.randint(7300, 25550))).date() if is_complete else None
        student_verified = random.random() < 0.3  # 30%是学生
        income = round(random.uniform(3000, 30000), 2) if is_complete else None
        max_amount = round(random.uniform(5000, 50000), 2)
        credit = round(random.uniform(60, 100), 2)
        loaned_amount = round(random.uniform(0, max_amount / 2), 2) if random.random() < 0.5 else 0
        
        created_at = datetime.datetime.fromisoformat(user["created_at"])
        updated_at = random_datetime(created_at, datetime.datetime.now())
        
        profiles.append({
            "id": i,
            "user_id": user["index"],
            "username": user["username"],
            "full_name": full_name,
            "phone_number": user["phone_number"],
            "gender": gender,
            "id_card_number": id_card_number,
            "id_card_expiry": id_card_expiry.isoformat() if id_card_expiry else None,
            "bank_account": bank_account,
            "profession": profession,
            "address": address,
            "date_of_birth": date_of_birth.isoformat() if date_of_birth else None,
            "student_verified": student_verified,
            "profile_picture": f"https://example.com/profiles/{user['id']}.jpg" if random.random() < 0.6 else None,
            "income": str(income) if income else None,
            "max_amount": str(max_amount),
            "credit": str(credit),
            "loaned_amount": str(loaned_amount),
            "is_profile_completed": is_complete,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        })
    
    return profiles

def generate_user_application_data(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """生成用户A卡评分卡数据"""
    applications = []
    
    for i, user in enumerate(users, 1):
        # 只有60%的用户有评分卡数据
        if random.random() > 0.6:
            continue
            
        age = random.randint(18, 60)
        real_name_verified = random.random() < 0.8  # 80%已实名认证
        is_student = random.random() < 0.3  # 30%是学生
        is_blacklisted = random.random() < 0.05  # 5%是黑名单用户
        is_unhealthy_4g_user = random.random() < 0.1  # 10%是4G不健康用户
        network_age_months = random.randint(1, 120)  # 1-120个月网龄
        last_payment_months_ago = random.randint(0, 6)
        last_payment_amount = round(random.uniform(10, 500), 2)
        avg_monthly_spending_6_months = round(random.uniform(50, 1000), 2)
        current_bill_total = round(random.uniform(50, 500), 2)
        current_account_balance = round(random.uniform(-100, 1000), 2)
        has_outstanding_payment = current_account_balance < 0
        call_fee_sensitivity = random.randint(1, 10)
        contacts_this_month = random.randint(5, 100)
        
        # 消费行为
        is_frequent_mall_visitor = random.random() < 0.4
        avg_mall_visits_3_months = random.randint(0, 20) if is_frequent_mall_visitor else random.randint(0, 3)
        visited_fuzhou_cangshan_wanda = random.random() < 0.3
        visited_fuzhou_sam_club = random.random() < 0.2
        watched_movie = random.random() < 0.5
        visited_scenic_spot = random.random() < 0.3
        used_sports_facility = random.random() < 0.25
        
        # APP使用情况
        online_shopping_app_usage = random.randint(0, 100)
        logistics_app_usage = random.randint(0, 50)
        finance_app_usage = random.randint(0, 30)
        video_app_usage = random.randint(0, 200)
        airplane_app_usage = random.randint(0, 10)
        train_app_usage = random.randint(0, 20)
        travel_info_app_usage = random.randint(0, 15)
        
        # 信用分
        credit_score = round(random.uniform(300, 850), 2)
        
        created_at = datetime.datetime.fromisoformat(user["created_at"])
        updated_at = random_datetime(created_at, datetime.datetime.now())
        
        applications.append({
            "id": len(applications) + 1,
            "user_id": user["index"],
            "real_name_verified": real_name_verified,
            "age": age,
            "is_student": is_student,
            "is_blacklisted": is_blacklisted,
            "is_unhealthy_4g_user": is_unhealthy_4g_user,
            "network_age_months": network_age_months,
            "last_payment_months_ago": last_payment_months_ago,
            "last_payment_amount": last_payment_amount,
            "avg_monthly_spending_6_months": avg_monthly_spending_6_months,
            "current_bill_total": current_bill_total,
            "current_account_balance": current_account_balance,
            "has_outstanding_payment": has_outstanding_payment,
            "call_fee_sensitivity": call_fee_sensitivity,
            "contacts_this_month": contacts_this_month,
            "is_frequent_mall_visitor": is_frequent_mall_visitor,
            "avg_mall_visits_3_months": avg_mall_visits_3_months,
            "visited_fuzhou_cangshan_wanda": visited_fuzhou_cangshan_wanda,
            "visited_fuzhou_sam_club": visited_fuzhou_sam_club,
            "watched_movie": watched_movie,
            "visited_scenic_spot": visited_scenic_spot,
            "used_sports_facility": used_sports_facility,
            "online_shopping_app_usage": online_shopping_app_usage,
            "logistics_app_usage": logistics_app_usage,
            "finance_app_usage": finance_app_usage,
            "video_app_usage": video_app_usage,
            "airplane_app_usage": airplane_app_usage,
            "train_app_usage": train_app_usage,
            "travel_info_app_usage": travel_info_app_usage,
            "credit_score": credit_score,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        })
    
    return applications

def generate_user_behavior_data(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """生成用户B卡评分卡数据"""
    behaviors = []
    
    for i, user in enumerate(users, 1):
        # 只有50%的用户有B卡数据
        if random.random() > 0.5:
            continue
            
        age = random.randint(18, 60)
        bank_cards_count = random.randint(1, 5)
        remote_transaction_months = random.randint(0, 6)
        internet_transaction_avg = round(random.uniform(0, 50), 2)
        financial_transaction_months = random.randint(0, 6)
        financial_transaction_avg_amount = round(random.uniform(0, 10000), 2)
        max_loan_amount_180_days = round(random.uniform(0, 50000), 2) if random.random() < 0.7 else 0
        min_loan_amount_180_days = round(random.uniform(0, max_loan_amount_180_days), 2) if max_loan_amount_180_days > 0 else 0
        apply_loan_company_number = random.randint(0, 5)
        
        created_at = datetime.datetime.fromisoformat(user["created_at"])
        updated_at = random_datetime(created_at, datetime.datetime.now())
        
        behaviors.append({
            "id": len(behaviors) + 1,
            "user_id": user["index"],
            "age": age,
            "bank_cards_count": bank_cards_count,
            "remote_transaction_months": remote_transaction_months,
            "internet_transaction_avg": internet_transaction_avg,
            "financial_transaction_months": financial_transaction_months,
            "financial_transaction_avg_amount": financial_transaction_avg_amount,
            "max_loan_amount_180_days": max_loan_amount_180_days,
            "min_loan_amount_180_days": min_loan_amount_180_days,
            "apply_loan_company_number": apply_loan_company_number,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        })
    
    return behaviors

def generate_user_sign_logs(users: List[Dict[str, Any]], count_per_user: int = 5) -> List[Dict[str, Any]]:
    """生成用户登录日志"""
    actions = ["登录", "登出"]
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
    ]
    ip_addresses = [
        "192.168.1.1", "10.0.0.1", "172.16.0.1",
        "123.45.67.89", "98.76.54.32", "111.222.333.444",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
    ]
    
    logs = []
    log_id = 1
    
    for user in users:
        user_logs_count = random.randint(1, count_per_user)
        user_created_at = datetime.datetime.fromisoformat(user["created_at"])
        
        for _ in range(user_logs_count):
            action = random.choice(actions)
            success = random.random() < 0.95  # 95%成功率
            message = None if success else random.choice(["密码错误", "账户已锁定", "网络连接超时"])
            created_at = random_datetime(user_created_at, datetime.datetime.now())
            
            logs.append({
                "id": log_id,
                "user_id": user["index"],
                "action": action,
                "ip_address": random.choice(ip_addresses),
                "user_agent": random.choice(user_agents),
                "success": success,
                "message": message,
                "created_at": created_at.isoformat()
            })
            log_id += 1
    
    return logs

def generate_article_data(count: int = 20) -> List[Dict[str, Any]]:
    """生成文章数据"""
    article_titles = [
        "如何提高个人信用分数", "贷款申请的常见误区", "大学生如何合理规划财务",
        "个人理财入门指南", "如何避免信用卡陷阱", "房贷vs车贷：如何选择",
        "小额贷款的优势与风险", "如何读懂贷款合同", "贷款逾期的后果与补救措施",
        "如何建立良好的信用记录", "投资理财的基本原则", "如何应对突发财务危机",
        "大学生创业贷款指南", "如何合理使用消费贷款", "贷款还款方式对比分析",
        "如何降低贷款成本", "个人破产法解读", "如何识别金融诈骗",
        "互联网金融产品分析", "如何制定个人预算计划"
    ]
    
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2024, 7, 1)
    
    articles = []
    for i in range(1, count + 1):
        title = article_titles[i - 1] if i <= len(article_titles) else f"金融知识分享 {i}"
        link = f"https://example.com/articles/{i}"
        publish_date = random_datetime(start_date, end_date)
        summary = f"{title}的摘要内容，介绍了相关的金融知识和实用技巧。"
        
        articles.append({
            "id": i,
            "link": link,
            "title": title,
            "publish_date": publish_date.isoformat(),
            "summary": summary
        })
    
    return articles

def generate_announcement_data(count: int = 10) -> List[Dict[str, Any]]:
    """生成公告数据"""
    announcement_titles = [
        "系统维护通知", "新功能上线公告", "利率调整通知",
        "节假日业务安排", "风险提示公告", "用户协议更新",
        "隐私政策变更", "客服热线调整", "安全提示",
        "活动预告"
    ]
    
    statuses = ["active", "inactive", "archived"]
    status_weights = [0.7, 0.2, 0.1]  # 70% 活跃, 20% 不活跃, 10% 归档
    
    authors = ["系统管理员", "客服中心", "风控部门", "产品团队", "技术支持"]
    
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2024, 7, 1)
    
    announcements = []
    for i in range(1, count + 1):
        title = announcement_titles[i - 1] if i <= len(announcement_titles) else f"重要通知 {i}"
        content = f"<h1>{title}</h1><p>尊敬的用户：</p><p>这是一条重要通知，请您仔细阅读。</p><p>详细内容...</p><p>如有疑问，请联系客服。</p>"
        publish_date = random_datetime(start_date, end_date)
        updated_at = random_datetime(publish_date, end_date)
        status = random.choices(statuses, weights=status_weights)[0]
        author = random.choice(authors)
        
        # 50%的公告有过期时间
        expiration_date = None
        if random.random() < 0.5:
            expiration_date = random_datetime(publish_date, publish_date + datetime.timedelta(days=90)).isoformat()
        
        announcements.append({
            "id": i,
            "title": title,
            "content": content,
            "publish_date": publish_date.isoformat(),
            "updated_at": updated_at.isoformat(),
            "status": status,
            "author": author,
            "expiration_date": expiration_date
        })
    
    return announcements

def generate_loan_records(users: List[Dict[str, Any]], profiles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """生成贷款记录"""
    loan_statuses = ["active", "completed", "defaulted", "overdue", "refused"]
    status_weights = [0.4, 0.3, 0.1, 0.1, 0.1]  # 40% 活跃, 30% 已完成, 10% 违约, 10% 逾期, 10% 拒绝
    
    repayment_methods = ["等额本金", "等额本息"]
    usages = ["教育", "医疗", "旅游", "装修", "消费", "创业", "其他"]
    auditors = ["张审核", "李审核", "王审核", "赵审核"]
    
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2024, 7, 1)
    
    loan_records = []
    
    # 为每个用户生成0-3条贷款记录
    for user, profile in zip(users, profiles):
        loan_count = random.randint(0, 3)
        
        for _ in range(loan_count):
            status = random.choices(loan_statuses, weights=status_weights)[0]
            amount = round(random.uniform(1000, float(profile["max_amount"])), 2)
            interest_rate = round(random.uniform(3.0, 15.0), 2)
            loan_term = random.choice([3, 6, 12, 24, 36])  # 贷款期限（月）
            repayment_method = random.choice(repayment_methods)
            usage = random.choice(usages)
            bank_account = profile["bank_account"] or generate_bank_account()
            
            created_at = random_datetime(start_date, end_date)
            updated_at = random_datetime(created_at, datetime.datetime.now())
            
            # 根据状态设置不同的还款金额
            repayment_amount = 0.0
            if status == "completed":
                repayment_amount = amount
            elif status == "active":
                # 随机还款进度
                progress = random.uniform(0.0, 0.9)  # 0% - 90%
                repayment_amount = round(amount * progress, 2)
            elif status == "overdue":
                # 部分还款
                progress = random.uniform(0.0, 0.7)  # 0% - 70%
                repayment_amount = round(amount * progress, 2)
            
            # 生成还款计划
            monthly_payment = round(amount / loan_term, 2)  # 简化计算，实际应考虑利息
            repayment_schedule = []
            for month in range(1, loan_term + 1):
                payment_date = created_at + datetime.timedelta(days=30 * month)
                repayment_schedule.append({
                    "month": month,
                    "amount": str(monthly_payment),
                    "date": payment_date.strftime("%Y-%m-%d"),
                    "status": "paid" if month <= (loan_term * repayment_amount / amount) else "unpaid"
                })
            
            # 审核相关信息
            income = profile["income"] or str(round(random.uniform(3000, 30000), 2))
            credit_score = random.randint(300, 850)
            auditor = random.choice(auditors) if status != "active" else None
            audit_time = random_datetime(created_at, created_at + datetime.timedelta(days=7)).isoformat() if auditor else None
            remark = None
            if status == "refused":
                remark = random.choice(["信用评分不足", "收入证明不足", "还款能力不足", "贷款用途不明确", "个人信息不完整"])
            
            loan_records.append({
                "id": len(loan_records) + 1,
                "user_id": user["index"],
                "amount": str(amount),
                "interest_rate": str(interest_rate),
                "loan_term": loan_term,
                "status": status,
                "repayment_method": repayment_method,
                "repayment_amount": str(repayment_amount),
                "repayment_schedule": json.dumps(repayment_schedule),
                "usage": usage,
                "bank_account": bank_account,
                "income": income,
                "credit_score": credit_score,
                "auditor": auditor,
                "audit_time": audit_time,
                "remark": remark,
                "created_at": created_at.isoformat(),
                "updated_at": updated_at.isoformat()
            })
    
    return loan_records

def generate_repayment_records(loan_records: List[Dict[str, Any]], users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """生成还款记录"""
    repayment_statuses = ["successful", "failed", "overdue"]
    status_weights = [0.9, 0.05, 0.05]  # 90% 成功, 5% 失败, 5% 逾期
    
    repayment_records = []
    
    for loan in loan_records:
        # 只为活跃、已完成和逾期的贷款生成还款记录
        if loan["status"] not in ["active", "completed", "overdue"]:
            continue
        
        # 解析还款计划
        repayment_schedule = json.loads(loan["repayment_schedule"])
        loan_created_at = datetime.datetime.fromisoformat(loan["created_at"])
        
        # 为已支付的月份生成还款记录
        for payment in repayment_schedule:
            if payment["status"] != "paid":
                continue
                
            status = random.choices(repayment_statuses, weights=status_weights)[0]
            amount = float(payment["amount"])
            payment_date = datetime.datetime.strptime(payment["date"], "%Y-%m-%d")
            
            # 随机添加一些波动到还款日期（提前或延后几天）
            payment_date_variance = payment_date + datetime.timedelta(days=random.randint(-3, 3))
            
            message = None
            if status == "failed":
                message = random.choice(["余额不足", "银行系统故障", "卡片已过期", "支付渠道异常"])
            elif status == "overdue":
                message = f"逾期{random.randint(1, 30)}天后支付"
            
            repayment_records.append({
                "id": len(repayment_records) + 1,
                "loan_id": loan["id"],
                "user_id": loan["user_id"],
                "amount": str(amount),
                "repayment_date": payment_date_variance.isoformat(),
                "status": status,
                "message": message
            })
    
    return repayment_records

def generate_interest_rates() -> List[Dict[str, Any]]:
    """生成利率数据"""
    return [{
        "id": 1,
        "interest_rate": "10.00"
    }]

def generate_ai_models(count: int = 5) -> List[Dict[str, Any]]:
    """生成AI模型数据"""
    model_names = ["信用评分模型", "风险预测模型", "欺诈检测模型", "用户画像模型", "贷款审批模型"]
    statuses = ["active", "current", "testing"]
    file_extensions = [".pkl", ".h5", ".joblib", ".pt", ".onnx"]
    
    start_date = datetime.datetime(2023, 1, 1)
    end_date = datetime.datetime(2024, 7, 1)
    
    models = []
    for i in range(1, count + 1):
        name = model_names[i - 1] if i <= len(model_names) else f"模型{i}"
        version = f"v{random.randint(1, 5)}.{random.randint(0, 9)}"
        file_extension = random.choice(file_extensions)
        file_path = f"/models/{name.replace(' ', '_')}_{version}{file_extension}"
        description = f"{name}用于{random.choice(['评估用户信用风险', '预测还款能力', '识别潜在欺诈行为', '分析用户行为模式', '辅助贷款审批决策'])}"
        technical_details = f"基于{random.choice(['随机森林', '梯度提升树', '深度神经网络', '逻辑回归', 'SVM'])}算法，使用{random.randint(10000, 1000000)}条训练数据"
        file_size = random.randint(1000000, 100000000)  # 1MB - 100MB
        status = random.choice(statuses)
        
        # 性能指标
        ks_value = round(random.uniform(0.3, 0.8), 2)
        bad_rate = round(random.uniform(0.01, 0.1), 3)
        accuracy = round(random.uniform(0.7, 0.95), 3)
        recall = round(random.uniform(0.6, 0.9), 3)
        precision = round(random.uniform(0.6, 0.9), 3)
        
        created_at = random_datetime(start_date, end_date)
        updated_at = random_datetime(created_at, datetime.datetime.now())
        
        models.append({
            "id": i,
            "name": name,
            "version": version,
            "file_path": file_path,
            "description": description,
            "technical_details": technical_details,
            "file_size": file_size,
            "file_extension": file_extension,
            "status": status,
            "ks_value": ks_value,
            "bad_rate": bad_rate,
            "accuracy": accuracy,
            "recall": recall,
            "precision": precision,
            "created_at": created_at.isoformat(),
            "updated_at": updated_at.isoformat()
        })
    
    return models

def generate_review_applications(loan_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """生成复审申请数据"""
    # 只为被拒绝的贷款生成复审申请
    refused_loans = [loan for loan in loan_records if loan["status"] == "refused"]
    
    statuses = ["review_pending", "review_approved", "review_rejected"]
    status_weights = [0.3, 0.4, 0.3]  # 30% 待审核, 40% 已批准, 30% 已拒绝
    
    priorities = ["high", "medium", "low"]
    priority_weights = [0.2, 0.6, 0.2]  # 20% 高优先级, 60% 中优先级, 20% 低优先级
    
    review_reasons = [
        "提供了新的收入证明",
        "已改善信用记录",
        "提供了额外担保",
        "降低了申请金额",
        "提供了更详细的贷款用途说明",
        "已完善个人信息"
    ]
    
    additional_docs_options = [
        ["收入证明.pdf"],
        ["工作证明.pdf", "银行流水.pdf"],
        ["担保人信息.pdf", "房产证明.pdf"],
        ["学历证明.pdf", "在职证明.pdf"],
        ["身份证正反面.jpg", "个人征信报告.pdf", "居住证明.pdf"]
    ]
    
    review_auditors = ["张复审", "李复审", "王复审"]
    
    review_applications = []
    
    for i, loan in enumerate(refused_loans):
        # 只有70%的被拒贷款会申请复审
        if random.random() > 0.7:
            continue
            
        status = random.choices(statuses, weights=status_weights)[0]
        priority = random.choices(priorities, weights=priority_weights)[0]
        review_reason = random.choice(review_reasons)
        additional_docs = random.choice(additional_docs_options)
        
        loan_created_at = datetime.datetime.fromisoformat(loan["created_at"])
        review_apply_time = random_datetime(loan_created_at, loan_created_at + datetime.timedelta(days=14))
        
        # 复审处理信息
        review_auditor = None
        review_time = None
        review_result = None
        review_comment = None
        
        if status != "review_pending":
            review_auditor = random.choice(review_auditors)
            review_time = random_datetime(review_apply_time, review_apply_time + datetime.timedelta(days=7)).isoformat()
            review_result = "approved" if status == "review_approved" else "rejected"
            
            if review_result == "approved":
                review_comment = random.choice([
                    "申请人提供的新证明材料符合要求",
                    "经重新评估，申请人具备还款能力",
                    "担保人资质良好，可以批准贷款",
                    "降低后的贷款金额风险可控"
                ])
            else:
                review_comment = random.choice([
                    "提供的补充材料仍不足以证明还款能力",
                    "信用记录改善不明显",
                    "担保人资质不符合要求",
                    "贷款用途仍不明确"
                ])
        
        review_applications.append({
            "id": len(review_applications) + 1,
            "original_audit_id": loan["id"],
            "applicant_name": f"用户{loan['user_id']}",
            "phone": generate_phone_number(),
            "id_card": generate_id_card(),
            "loan_amount": loan["amount"],
            "loan_purpose": loan["usage"],
            "original_result": "refused",
            "original_reason": loan["remark"],
            "original_auditor": loan["auditor"],
            "original_audit_time": loan["audit_time"],
            "review_reason": review_reason,
            "review_apply_time": review_apply_time.isoformat(),
            "status": status,
            "priority": priority,
            "additional_docs": json.dumps(additional_docs),
            "review_auditor": review_auditor,
            "review_time": review_time,
            "review_result": review_result,
            "review_comment": review_comment,
            "created_at": review_apply_time.isoformat(),
            "updated_at": (review_time and datetime.datetime.fromisoformat(review_time) or review_apply_time).isoformat()
        })
    
    return review_applications

# 生成所有模拟数据
def generate_all_mock_data():
    """生成所有模拟数据并返回"""
    # 生成用户相关数据
    users = generate_user_auth_data(20)  # 生成20个用户
    profiles = generate_user_profile_data(users)
    applications = generate_user_application_data(users)
    behaviors = generate_user_behavior_data(users)
    sign_logs = generate_user_sign_logs(users)
    
    # 生成文章和公告
    articles = generate_article_data()
    announcements = generate_announcement_data()
    
    # 生成贷款相关数据
    loan_records = generate_loan_records(users, profiles)
    repayment_records = generate_repayment_records(loan_records, users)
    interest_rates = generate_interest_rates()
    
    # 生成模型和复审数据
    ai_models = generate_ai_models()
    review_applications = generate_review_applications(loan_records)
    
    return {
        "users": users,
        "profiles": profiles,
        "applications": applications,
        "behaviors": behaviors,
        "sign_logs": sign_logs,
        "articles": articles,
        "announcements": announcements,
        "loan_records": loan_records,
        "repayment_records": repayment_records,
        "interest_rates": interest_rates,
        "ai_models": ai_models,
        "review_applications": review_applications
    }

# 如果直接运行此脚本，则生成数据并打印
if __name__ == "__main__":
    mock_data = generate_all_mock_data()
    print(json.dumps(mock_data, indent=2, ensure_ascii=False))