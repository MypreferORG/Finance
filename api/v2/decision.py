# -*- coding: utf-8 -*-
"""
# @Create on : 2025/09/14
# @Author : Myprefer
# @Des: 决策引擎API路由
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import date

from schemas.decision import (
    DecisionRuleCreate, DecisionRuleUpdate, DecisionRuleResponse, DecisionRuleList,
    RuleValidationRequest, RuleValidationResponse,
    ExecutionRequest, ExecutionResponse,
    TestCase, TestResponse,
    ExecutionHistoryResponse, ExecutionHistoryList,
    StatisticsResponse, SuccessResponse, ErrorResponse
)
from services.decision_service import DecisionEngineService

router = APIRouter()


# 规则管理接口
@router.get("/rules", response_model=SuccessResponse, summary="获取规则列表")
async def get_rules(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    status: Optional[str] = Query(None, description="规则状态筛选"),
    keyword: Optional[str] = Query(None, description="关键字搜索")
):
    """获取规则列表，支持分页和筛选"""
    try:
        rules, total = await DecisionEngineService.get_rules(skip, limit, status, keyword)
        
        rule_list = DecisionRuleList(
            data=[DecisionRuleResponse.from_orm(rule) for rule in rules],
            total=total,
            skip=skip,
            limit=limit
        )
        
        return SuccessResponse(data=rule_list.dict(), message="获取成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rules", response_model=SuccessResponse, summary="创建规则")
async def create_rule(rule_data: DecisionRuleCreate):
    """创建新的决策规则"""
    try:
        rule = await DecisionEngineService.create_rule(rule_data, "system")
        return SuccessResponse(
            data=DecisionRuleResponse.from_orm(rule).dict(),
            message="创建成功"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules/{rule_id}", response_model=SuccessResponse, summary="获取规则详情")
async def get_rule(rule_id: str):
    """获取指定规则的详细信息"""
    try:
        rule = await DecisionEngineService.get_rule(rule_id)
        if not rule:
            raise HTTPException(status_code=404, detail="规则不存在")
            
        return SuccessResponse(
            data=DecisionRuleResponse.from_orm(rule).dict(),
            message="获取成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/rules/{rule_id}", response_model=SuccessResponse, summary="更新规则")
async def update_rule(rule_id: str, rule_data: DecisionRuleUpdate):
    """更新指定规则"""
    try:
        rule = await DecisionEngineService.update_rule(rule_id, rule_data)
        if not rule:
            raise HTTPException(status_code=404, detail="规则不存在")
            
        return SuccessResponse(
            data=DecisionRuleResponse.from_orm(rule).dict(),
            message="更新成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/rules/{rule_id}", response_model=SuccessResponse, summary="删除规则")
async def delete_rule(rule_id: str):
    """删除指定规则"""
    try:
        success = await DecisionEngineService.delete_rule(rule_id)
        if not success:
            raise HTTPException(status_code=404, detail="规则不存在")
            
        return SuccessResponse(data=None, message="删除成功")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 规则验证接口
@router.post("/rules/validate", response_model=SuccessResponse, summary="验证规则")
async def validate_rule(validation_data: RuleValidationRequest):
    """验证规则的完整性和正确性"""
    try:
        result = DecisionEngineService.validate_rule(validation_data)
        return SuccessResponse(data=result, message="验证完成")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 规则执行接口
@router.post("/rules/{rule_id}/execute", response_model=SuccessResponse, summary="执行规则")
async def execute_rule(rule_id: str, execution_data: ExecutionRequest):
    """执行指定规则"""
    try:
        result = await DecisionEngineService.execute_rule(rule_id, execution_data.input_data)
        return SuccessResponse(data=result, message="执行完成")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 规则测试接口
@router.post("/rules/{rule_id}/test", response_model=SuccessResponse, summary="测试规则")
async def test_rule(rule_id: str, test_cases: List[TestCase]):
    """使用测试用例批量测试规则"""
    try:
        result = await DecisionEngineService.test_rule(rule_id, test_cases)
        return SuccessResponse(data=result, message="测试完成")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 执行历史接口
@router.get("/execution-history", response_model=SuccessResponse, summary="获取执行历史")
async def get_execution_history(
    rule_id: Optional[str] = Query(None, description="规则ID筛选"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="每页记录数"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期")
):
    """获取规则执行历史记录"""
    try:
        # 处理日期参数，如果是空字符串则设为 None
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date and start_date.strip():
            try:
                from datetime import datetime
                parsed_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="start_date 格式错误，应为 YYYY-MM-DD")
                
        if end_date and end_date.strip():
            try:
                from datetime import datetime
                parsed_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="end_date 格式错误，应为 YYYY-MM-DD")
        
        # 处理 rule_id，如果是空字符串则设为 None
        processed_rule_id = rule_id if rule_id and rule_id.strip() else None
        
        executions, total = await DecisionEngineService.get_execution_history(
            processed_rule_id, skip, limit, parsed_start_date, parsed_end_date
        )
        
        history_list = ExecutionHistoryList(
            data=[ExecutionHistoryResponse.from_orm(execution) for execution in executions],
            total=total,
            skip=skip,
            limit=limit
        )
        
        return SuccessResponse(data=history_list.dict(), message="获取成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 统计数据接口
@router.get("/statistics", response_model=SuccessResponse, summary="获取统计数据")
async def get_statistics():
    """获取决策引擎的统计数据"""
    try:
        stats = await DecisionEngineService.get_statistics()
        return SuccessResponse(data=stats, message="获取成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 健康检查接口
@router.get("/health", response_model=SuccessResponse, summary="健康检查")
async def health_check():
    """决策引擎健康检查"""
    return SuccessResponse(
        data={"status": "healthy", "service": "decision-engine"},
        message="服务正常"
    )