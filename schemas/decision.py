# -*- coding: utf-8 -*-
"""
# @Create on : 2025/09/14
# @Author : Myprefer
# @Des: 决策引擎Schema模型
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum


class RuleStatus(str, Enum):
    """规则状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"


class ExecutionStatus(str, Enum):
    """执行状态枚举"""
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class TestStatus(str, Enum):
    """测试状态枚举"""
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"


class NodeType(str, Enum):
    """节点类型枚举"""
    CONDITION = "condition"
    ACTION = "action"
    DECISION = "decision"
    DATA_SOURCE = "data_source"
    MODEL = "model"


class VariableType(str, Enum):
    """变量类型枚举"""
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    DATE = "date"


# 基础节点和边模型
class Position(BaseModel):
    """节点位置"""
    x: float
    y: float


class RuleNode(BaseModel):
    """规则节点"""
    id: str
    type: NodeType
    position: Position
    data: Dict[str, Any]


class RuleEdge(BaseModel):
    """规则边"""
    id: str
    source: str
    target: str
    type: Optional[str] = "default"
    data: Optional[Dict[str, Any]] = None


class RuleVariable(BaseModel):
    """规则变量"""
    name: str
    type: VariableType
    description: Optional[str] = None
    default_value: Optional[Any] = None
    category: Optional[str] = None


# 规则相关Schema
class DecisionRuleBase(BaseModel):
    """决策规则基础模型"""
    name: str
    description: Optional[str] = None
    nodes: List[RuleNode]
    edges: List[RuleEdge]
    variables: List[RuleVariable]
    status: RuleStatus = RuleStatus.DRAFT


class DecisionRuleCreate(DecisionRuleBase):
    """创建决策规则"""
    pass


class DecisionRuleUpdate(DecisionRuleBase):
    """更新决策规则"""
    pass


class DecisionRuleResponse(DecisionRuleBase):
    """决策规则响应"""
    id: str
    version: str
    created_at: datetime
    updated_at: datetime
    created_by: str

    class Config:
        from_attributes = True


class DecisionRuleList(BaseModel):
    """规则列表响应"""
    data: List[DecisionRuleResponse]
    total: int
    skip: int
    limit: int


# 规则验证相关Schema
class RuleValidationRequest(BaseModel):
    """规则验证请求"""
    nodes: List[RuleNode]
    edges: List[RuleEdge]
    variables: List[RuleVariable]


class ValidationError(BaseModel):
    """验证错误"""
    code: str
    message: str
    node_id: Optional[str] = None


class RuleValidationResponse(BaseModel):
    """规则验证响应"""
    valid: bool
    errors: List[str] = []
    warnings: List[str] = []
    suggestions: List[str] = []


# 规则执行相关Schema
class ExecutionRequest(BaseModel):
    """执行请求"""
    input_data: Dict[str, Any]


class NodeResult(BaseModel):
    """节点执行结果"""
    node_id: str
    result: Any
    execution_time: Optional[float] = None
    error: Optional[str] = None


class ExecutionResult(BaseModel):
    """执行结果"""
    decision: str
    confidence: Optional[float] = None
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    approved_amount: Optional[float] = None
    reason: Optional[str] = None


class ExecutionResponse(BaseModel):
    """执行响应"""
    rule_id: str
    execution_id: str
    result: ExecutionResult
    execution_path: List[str]
    node_results: Dict[str, Any]
    execution_time: float
    created_at: datetime


class ExecutionHistoryResponse(BaseModel):
    """执行历史响应"""
    id: str
    rule_id: str
    rule_name: str
    input_data: Dict[str, Any]
    result: ExecutionResult
    execution_time: float
    status: ExecutionStatus
    created_at: datetime

    class Config:
        from_attributes = True


class ExecutionHistoryList(BaseModel):
    """执行历史列表"""
    data: List[ExecutionHistoryResponse]
    total: int
    skip: int
    limit: int


# 测试相关Schema
class TestCase(BaseModel):
    """测试用例"""
    name: str
    input_data: Dict[str, Any]
    expected_result: Dict[str, Any]


class TestCaseResult(BaseModel):
    """测试用例结果"""
    test_case: TestCase
    result: ExecutionResponse
    status: TestStatus
    match_expected: bool


class TestResponse(BaseModel):
    """测试响应"""
    total: int
    success: int
    failure: int
    success_rate: float
    results: List[TestCaseResult]


# 统计相关Schema
class RuleStats(BaseModel):
    """规则统计"""
    total: int
    active: int
    draft: int
    disabled: int


class ExecutionStats(BaseModel):
    """执行统计"""
    total: int
    todayExecutions: int
    last7Days: int
    last30Days: int


class PerformanceStats(BaseModel):
    """性能统计"""
    avgResponseTime: float  # 毫秒
    successRate: float
    errorRate: float


class RecentExecution(BaseModel):
    """最近执行"""
    id: str
    rule_name: str
    result: Dict[str, Any]
    execution_time: float
    created_at: datetime


class StatisticsResponse(BaseModel):
    """统计响应"""
    total_rules: int
    active_rules: int
    draft_rules: int
    disabled_rules: int
    total_executions: int
    today_executions: int
    avg_execution_time: float
    success_rate: float
    rule_count: RuleStats
    execution_stats: ExecutionStats
    performance: PerformanceStats
    recent_executions: List[RecentExecution]


# 状态更新相关Schema
class RuleStatusUpdate(BaseModel):
    """规则状态更新请求"""
    status: RuleStatus


class RuleStatusResponse(BaseModel):
    """规则状态更新响应"""
    id: str
    name: str
    status: RuleStatus
    updated_at: datetime

    class Config:
        from_attributes = True


class BatchStatusUpdate(BaseModel):
    """批量状态更新请求"""
    rule_ids: List[str]
    status: RuleStatus


class BatchUpdateResult(BaseModel):
    """批量更新单个结果"""
    id: str
    name: Optional[str] = None
    status: Optional[RuleStatus] = None
    error: Optional[str] = None


class BatchStatusResponse(BaseModel):
    """批量状态更新响应"""
    updated_count: int
    failed_count: int
    updated_rules: List[BatchUpdateResult]
    failed_rules: List[BatchUpdateResult]


# 通用响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool = True
    message: str = "操作成功"
    timestamp: datetime = Field(default_factory=datetime.now)


class SuccessResponse(BaseResponse):
    """成功响应"""
    data: Optional[Any] = None


class ErrorResponse(BaseResponse):
    """错误响应"""
    success: bool = False
    code: Optional[int] = None
    detail: Optional[str] = None