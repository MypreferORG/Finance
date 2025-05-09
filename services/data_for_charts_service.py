from datetime import datetime, timedelta
from typing import List, Dict, Any
from decimal import Decimal
from tortoise.expressions import Q
from tortoise.functions import Count, Sum

from models.loan import LoanRecord
from models.user import UserAuth, UserProfile

async def get_thisWeekVolume() -> List[float]:
    """获取近七天每日成交量数据
    
    Returns:
        List[float]: 近七天的每日成交量列表
    """
    # 获取最近7天的日期
    today = datetime.now().date()
    dates = []
    for i in range(6, -1, -1):
        dates.append(today - timedelta(days=i))
    
    daily_volumes = []
    for date in dates:
        result = await LoanRecord.filter(
            created_at__gte=date,
            created_at__lt=date + timedelta(days=1),
            status__in=["active", "completed"]
        ).annotate(total=Sum('amount')).first()

        # 提取 total 字段，失败则设为 0.0
        volume = float(result.total) if result and result.total is not None else 0.0
        daily_volumes.append(volume)
    
    return daily_volumes

async def get_totalVolume() -> List[float]:
    """获取近七天累计成交量数据
    
    Returns:
        List[float]: 近七天的累计成交量列表
    """
    # 获取最近7天的日期
    today = datetime.now().date()
    dates = []
    for i in range(6, -1, -1):
        dates.append(today - timedelta(days=i))
    
    total_volumes = []
    for i, date in enumerate(dates):
        # 查询从第一天到当前日期的累计贷款总额
        start_date = dates[0]  # 第一天
        end_date = date + timedelta(days=1)  # 当前日期的下一天
        
        result = await LoanRecord.filter(
            created_at__gte=start_date,
            created_at__lt=end_date,
            status__in=["active", "completed"]
        ).annotate(total=Sum('amount')).first()
        
        # 提取 total 字段，失败则设为 0.0
        volume = float(result.total) if result and result.total is not None else 0.0
        total_volumes.append(volume)
    
    return total_volumes

async def get_loanNum() -> List[int]:
    """获取各金额区间的贷款人数
    
    Returns:
        List[int]: 各金额区间的贷款人数列表，顺序为：
        [5000元~9999元, 3000元~4999元, 10000元~19999元, 1000元~1999元, 2000元~2999元, 20000元~50000元, 0~999元]
    """
    
    # 不是我设置的怪范围，前端的顺序就是这样（
    # 定义金额区间 
    amount_ranges = [
        (5000, 9999),    # 5000元~9999元
        (3000, 4999),    # 3000元~4999元
        (10000, 19999),  # 10000元~19999元
        (1000, 1999),    # 1000元~1999元
        (2000, 2999),    # 2000元~2999元
        (20000, 50000),  # 20000元~50000元
        (0, 999)         # 0~999元
    ]
    
    loan_numbers = []
    for min_amount, max_amount in amount_ranges:
        # 查询每个区间的贷款人数
        count = await LoanRecord.filter(
            amount__gte=min_amount,
            amount__lt=max_amount + 1,  # 加1是为了包含上限值
            status__in=["active", "completed"]
        ).count()
        
        loan_numbers.append(count)
    
    return loan_numbers

async def get_passNum() -> List[int]:
    """获取近六天每天的通过人数，从5天前到今天
    
    Returns:
        List[int]: 近六天每天的通过人数列表，顺序为[5天前, 4天前, 3天前, 2天前, 1天前, 今天]
    """
    # 获取最近6天的日期，从5天前到今天
    today = datetime.now().date()
    dates = []
    for i in range(5, -1, -1):
        dates.append(today - timedelta(days=i))
    
    pass_numbers = []
    for date in dates:
        count = await LoanRecord.filter(
            created_at__gte=date,
            created_at__lt=date + timedelta(days=1),
            status="active"  # 通过状态
        ).count()
        pass_numbers.append(count)
    
    return pass_numbers

async def get_refuseNum() -> List[int]:
    """获取近六天每天的拒绝人数，从5天前到今天
    
    Returns:
        List[int]: 近六天每天的拒绝人数列表，顺序为[5天前, 4天前, 3天前, 2天前, 1天前, 今天]
    """
    # 获取最近6天的日期，从5天前到今天
    today = datetime.now().date()
    dates = []
    for i in range(5, -1, -1):
        dates.append(today - timedelta(days=i))
    
    refuse_numbers = []
    for date in dates:
        count = await LoanRecord.filter(
            created_at__gte=date,
            created_at__lt=date + timedelta(days=1),
            status="refused" 
        ).count()
        refuse_numbers.append(count)
    
    return refuse_numbers

async def get_overdueNum() -> List[int]:
    """获取近六天每天的逾期人数，从5天前到今天
    
    Returns:
        List[int]: 近六天每天的逾期人数列表，顺序为[5天前, 4天前, 3天前, 2天前, 1天前, 今天]
    """
    # 获取最近6天的日期，从5天前到今天
    today = datetime.now().date()
    dates = []
    for i in range(5, -1, -1):
        dates.append(today - timedelta(days=i))
    
    overdue_numbers = []
    for date in dates:
        count = await LoanRecord.filter(
            created_at__gte=date,
            created_at__lt=date + timedelta(days=1),
            status="overdue"  # 逾期状态
        ).count()
        overdue_numbers.append(count)
    
    return overdue_numbers

async def get_numOfPeople() -> List[int]:
    """获取各城市贷款人数数据
    
    Returns:
        List[int]: 各城市贷款人数列表，顺序为：
        [北京, 上海, 广州, 西宁, 拉萨, 西安, 银川, 潍坊, 哈尔滨, 厦门, 郑州, 太原, 成都]
    """
    # 定义城市列表，保持与前端一致的顺序
    cities = [
        "北京", "上海", "广州", "西宁", "拉萨", "西安", "银川", 
        "潍坊", "哈尔滨", "厦门", "郑州", "太原", "成都"
    ]
    
    # 查询每个城市的贷款人数
    city_counts = []
    for city in cities:
        count = await LoanRecord.filter(
            # 应该没问题，这里需要访问两次外键，第一次是loanRecord的user，第二次是user的user_profiles
            Q(user__user_profiles__address__startswith=city) |  # 以城市名开头
            Q(user__user_profiles__address__contains=f"{city}市") |  # 包含"城市名+市"
            Q(user__user_profiles__address__contains=f"{city}省"),  # 包含"城市名+省"
            status__in=["active", "completed"]
        ).count()
        city_counts.append(count)
    
    return city_counts

# todo: 右下角数据
# 需要的是PSI值，召回率，模型精度，AUC，坏账率，KS值