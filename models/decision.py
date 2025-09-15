# -*- coding: utf-8 -*-
"""
# @Create on : 2025/09/14
# @Author : Myprefer
# @Des: 决策引擎数据模型
"""

from tortoise import fields
from tortoise.models import Model
from typing import Dict, List, Any
import json


class DecisionRule(Model):
    """决策规则模型"""
    id = fields.CharField(max_length=50, pk=True, description="规则ID")
    name = fields.CharField(max_length=100, description="规则名称")
    description = fields.TextField(null=True, description="规则描述")
    nodes = fields.JSONField(description="规则节点数据")
    edges = fields.JSONField(description="规则边数据")
    variables = fields.JSONField(description="规则变量数据")
    status = fields.CharField(
        max_length=20, 
        default="active", 
        description="规则状态: draft/active/inactive"
    )
    version = fields.CharField(max_length=20, default="1.0.0", description="版本号")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")
    created_by = fields.CharField(max_length=50, description="创建者ID")

    class Meta:
        table = "decision_rules"
        indexes = [("status",), ("created_by",), ("name",)]

    def __str__(self):
        return f"DecisionRule(id={self.id}, name={self.name}, status={self.status})"


class DecisionExecution(Model):
    """决策执行记录模型"""
    id = fields.CharField(max_length=50, pk=True, description="执行ID")
    rule_id = fields.CharField(max_length=50, description="规则ID")
    rule_name = fields.CharField(max_length=100, description="规则名称")
    input_data = fields.JSONField(description="输入数据")
    result = fields.JSONField(description="执行结果")
    execution_path = fields.JSONField(description="执行路径")
    node_results = fields.JSONField(description="节点执行结果")
    execution_time = fields.FloatField(description="执行耗时(秒)")
    status = fields.CharField(
        max_length=20, 
        default="completed", 
        description="执行状态: completed/failed/timeout"
    )
    error_message = fields.TextField(null=True, description="错误信息")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")

    class Meta:
        table = "decision_executions"
        indexes = [("rule_id",), ("status",), ("created_at",)]

    def __str__(self):
        return f"DecisionExecution(id={self.id}, rule_id={self.rule_id}, status={self.status})"


class DecisionTestCase(Model):
    """决策测试用例模型"""
    id = fields.IntField(pk=True)
    rule_id = fields.CharField(max_length=50, description="规则ID")
    name = fields.CharField(max_length=100, description="测试用例名称")
    input_data = fields.JSONField(description="测试输入数据")
    expected_result = fields.JSONField(description="期望结果")
    actual_result = fields.JSONField(null=True, description="实际结果")
    status = fields.CharField(
        max_length=20, 
        null=True, 
        description="测试状态: success/failure/pending"
    )
    match_expected = fields.BooleanField(null=True, description="是否匹配期望结果")
    execution_time = fields.FloatField(null=True, description="执行耗时(秒)")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "decision_test_cases"
        indexes = [("rule_id",), ("status",)]

    def __str__(self):
        return f"DecisionTestCase(id={self.id}, name={self.name}, status={self.status})"


class DecisionStatistics(Model):
    """决策统计数据模型"""
    id = fields.IntField(pk=True)
    date = fields.DateField(description="统计日期")
    rule_id = fields.CharField(max_length=50, null=True, description="规则ID")
    total_executions = fields.IntField(default=0, description="总执行次数")
    success_executions = fields.IntField(default=0, description="成功执行次数")
    failed_executions = fields.IntField(default=0, description="失败执行次数")
    avg_execution_time = fields.FloatField(default=0.0, description="平均执行时间")
    created_at = fields.DatetimeField(auto_now_add=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        table = "decision_statistics"
        indexes = [("date",), ("rule_id",)]

    def __str__(self):
        return f"DecisionStatistics(date={self.date}, rule_id={self.rule_id})"