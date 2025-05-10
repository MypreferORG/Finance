from fastapi import APIRouter
from typing import List

from services.data_for_charts_service import (
    get_thisWeekVolume,
    get_totalVolume,
    get_loanNum,
    get_passNum,
    get_refuseNum,
    get_overdueNum,
    get_numOfPeople
)

router = APIRouter(prefix="/charts", tags=["图表数据"])

@router.get("/weekly-volume", response_model=List[float])
async def get_weekly_volume():
    """获取近七天每日成交量数据"""
    return await get_thisWeekVolume()

@router.get("/total-volume", response_model=List[float])
async def get_total_volume():
    """获取近七天累计成交量数据"""
    return await get_totalVolume()

@router.get("/loan-numbers", response_model=List[int])
async def get_loan_numbers():
    """获取各金额区间的贷款人数"""
    return await get_loanNum()

@router.get("/pass-numbers", response_model=List[int])
async def get_pass_numbers():
    """获取近六天每天的通过人数"""
    return await get_passNum()

@router.get("/refuse-numbers", response_model=List[int])
async def get_refuse_numbers():
    """获取近六天每天的拒绝人数"""
    return await get_refuseNum()

@router.get("/overdue-numbers", response_model=List[int])
async def get_overdue_numbers():
    """获取近六天每天的逾期人数"""
    return await get_overdueNum()

@router.get("/city-numbers", response_model=List[int])
async def get_city_numbers():
    """获取各城市贷款人数数据"""
    return await get_numOfPeople() 