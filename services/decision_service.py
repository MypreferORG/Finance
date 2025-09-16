# -*- coding: utf-8 -*-
"""
# @Create on : 2025/09/14
# @Author : Myprefer
# @Des: 决策引擎服务
"""

import uuid
import json
import time
import re
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple
from tortoise.expressions import Q
from tortoise.transactions import in_transaction

from models.decision import DecisionRule, DecisionExecution, DecisionTestCase, DecisionStatistics
from schemas.decision import (
    DecisionRuleCreate, DecisionRuleUpdate, RuleValidationRequest,
    ExecutionRequest, TestCase, RuleStatus, ExecutionStatus, NodeType,
    RuleStatusUpdate, BatchStatusUpdate, BatchUpdateResult,
    TestCaseCreate, TestCaseUpdate
)
from pydantic import BaseModel
from enum import Enum


class DecisionEngineService:
    """决策引擎服务类"""

    @staticmethod
    async def get_rules(skip: int = 0, limit: int = 100, status: Optional[str] = None, 
                       keyword: Optional[str] = None) -> Tuple[List[DecisionRule], int]:
        """获取规则列表"""
        query = DecisionRule.all()
        
        if status:
            query = query.filter(status=status)
            
        if keyword:
            query = query.filter(
                Q(name__icontains=keyword) | 
                Q(description__icontains=keyword)
            )
            
        total = await query.count()
        rules = await query.offset(skip).limit(limit).order_by('-created_at')
        
        return rules, total

    @staticmethod
    async def create_rule(rule_data: DecisionRuleCreate, created_by: str) -> DecisionRule:
        """创建规则"""
        rule_id = f"rule_{uuid.uuid4().hex[:8]}"
        # 将 Pydantic / Enum 转换为可 JSON 序列化的原生结构
        serialized_nodes = DecisionEngineService._to_serializable(rule_data.nodes)
        serialized_edges = DecisionEngineService._to_serializable(rule_data.edges)
        serialized_variables = DecisionEngineService._to_serializable(rule_data.variables)

        rule = await DecisionRule.create(
            id=rule_id,
            name=rule_data.name,
            description=rule_data.description,
            nodes=serialized_nodes,
            edges=serialized_edges,
            variables=serialized_variables,
            status=rule_data.status.value,
            created_by=created_by
        )

        return rule

    @staticmethod
    async def get_rule(rule_id: str) -> Optional[DecisionRule]:
        """获取规则详情"""
        return await DecisionRule.get_or_none(id=rule_id)

    @staticmethod
    async def update_rule(rule_id: str, rule_data: DecisionRuleUpdate) -> Optional[DecisionRule]:
        """更新规则"""
        rule = await DecisionRule.get_or_none(id=rule_id)
        if not rule:
            return None
            
        # 更新版本号
        version_parts = rule.version.split('.')
        version_parts[-1] = str(int(version_parts[-1]) + 1)
        new_version = '.'.join(version_parts)
        # 序列化更新数据
        rule.name = rule_data.name
        rule.description = rule_data.description
        rule.nodes = DecisionEngineService._to_serializable(rule_data.nodes)
        rule.edges = DecisionEngineService._to_serializable(rule_data.edges)
        rule.variables = DecisionEngineService._to_serializable(rule_data.variables)
        rule.status = rule_data.status.value
        rule.version = new_version

        await rule.save()
        return rule

    @staticmethod
    async def delete_rule(rule_id: str) -> bool:
        """删除规则"""
        rule = await DecisionRule.get_or_none(id=rule_id)
        if not rule:
            return False
            
        await rule.delete()
        return True

    @staticmethod
    async def update_rule_status(rule_id: str, status_update: RuleStatusUpdate) -> Optional[DecisionRule]:
        """更新规则状态"""
        rule = await DecisionRule.get_or_none(id=rule_id)
        if not rule:
            return None
            
        rule.status = status_update.status.value
        await rule.save()
        return rule

    @staticmethod
    async def batch_update_rule_status(batch_update: BatchStatusUpdate) -> Dict[str, Any]:
        """批量更新规则状态"""
        updated_rules = []
        failed_rules = []
        
        for rule_id in batch_update.rule_ids:
            try:
                rule = await DecisionRule.get_or_none(id=rule_id)
                if not rule:
                    failed_rules.append(BatchUpdateResult(
                        id=rule_id,
                        error="规则不存在或已被删除"
                    ))
                    continue
                    
                rule.status = batch_update.status.value
                await rule.save()
                
                updated_rules.append(BatchUpdateResult(
                    id=rule.id,
                    name=rule.name,
                    status=RuleStatus(rule.status)
                ))
                
            except Exception as e:
                failed_rules.append(BatchUpdateResult(
                    id=rule_id,
                    error=str(e)
                ))
                
        return {
            "updated_count": len(updated_rules),
            "failed_count": len(failed_rules),
            "updated_rules": updated_rules,
            "failed_rules": failed_rules
        }

    @staticmethod
    def validate_rule(validation_data: RuleValidationRequest) -> Dict[str, Any]:
        """验证规则"""
        errors = []
        warnings = []
        suggestions = []
        
        nodes = validation_data.nodes
        edges = validation_data.edges
        variables = validation_data.variables
        
        # 检查是否有开始节点
        start_nodes = [node for node in nodes if getattr(node.type, 'value', node.type) == NodeType.DATA_SOURCE.value]
        if not start_nodes:
            errors.append("缺少数据源节点作为开始节点")
            
        # 检查是否有决策节点
        decision_nodes = [node for node in nodes if getattr(node.type, 'value', node.type) == NodeType.DECISION.value]
        if not decision_nodes:
            warnings.append("建议添加决策节点作为输出")
            
        # 检查节点连接
        node_ids = {node.id for node in nodes}
        for edge in edges:
            if edge.source not in node_ids:
                errors.append(f"边 {edge.id} 的源节点 {edge.source} 不存在")
            if edge.target not in node_ids:
                errors.append(f"边 {edge.id} 的目标节点 {edge.target} 不存在")
                
        # 检查条件节点的表达式
        for node in nodes:
            if getattr(node.type, 'value', node.type) == NodeType.CONDITION.value and "condition" in node.data:
                condition = node.data["condition"]
                if not DecisionEngineService._validate_condition_expression(condition):
                    errors.append(f"节点 {node.id} 的条件表达式语法错误")
                    
        # 检查变量定义
        # used_variables = set()
        # for node in nodes:
        #     if node.type == "condition" and "condition" in node.data:
        #         condition = node.data["condition"]
        #         used_variables.update(DecisionEngineService._extract_variables(condition))
                
        # defined_variables = {var.name for var in variables}
        # undefined_variables = used_variables - defined_variables
        # if undefined_variables:
        #     errors.append(f"使用了未定义的变量: {', '.join(undefined_variables)}")
            
        # 建议
        if len(nodes) < 3:
            suggestions.append("建议增加更多的处理节点以完善决策逻辑")
            
        valid = len(errors) == 0
        
        return {
            "valid": valid,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }

    @staticmethod
    def _to_serializable(obj: Any):
        """将 Pydantic BaseModel / Enum / 复杂嵌套结构转换为原生可 JSON 序列化结构。

        解决问题: 直接把 Pydantic 模型列表传给 Tortoise JSONField 会触发 TypeError: Object of type RuleNode is not JSON serializable。
        """
        if obj is None:
            return None
        # Enum -> value
        if isinstance(obj, Enum):
            return obj.value
        # Pydantic BaseModel
        if isinstance(obj, BaseModel):
            data = obj.dict()
            return {k: DecisionEngineService._to_serializable(v) for k, v in data.items()}
        # list / tuple
        if isinstance(obj, (list, tuple)):
            return [DecisionEngineService._to_serializable(i) for i in obj]
        # dict
        if isinstance(obj, dict):
            return {k: DecisionEngineService._to_serializable(v) for k, v in obj.items()}
        # 基本类型
        return obj

    @staticmethod
    def _validate_condition_expression(condition: str) -> bool:
        """验证条件表达式语法"""
        try:
            # 简单的语法检查，替换变量为值进行解析
            test_condition = re.sub(r'[a-zA-Z_][a-zA-Z0-9_.]*', '1', condition)
            test_condition = test_condition.replace('&&', ' and ').replace('||', ' or ').replace('!', ' not ')
            compile(test_condition, '<string>', 'eval')
            return True
        except:
            return False

    @staticmethod
    def _extract_variables(condition: str) -> List[str]:
        """从条件表达式中提取变量名"""
        pattern = r'[a-zA-Z_][a-zA-Z0-9_.]*'
        variables = re.findall(pattern, condition)
        # 过滤掉 JavaScript 关键字
        keywords = {'true', 'false', 'null', 'undefined', 'and', 'or', 'not'}
        return [var for var in variables if var not in keywords]

    @staticmethod
    async def execute_rule(rule_id: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行规则"""
        start_time = time.time()
        execution_id = f"exec_{uuid.uuid4().hex[:8]}"
        
        rule = await DecisionRule.get_or_none(id=rule_id)
        if not rule:
            raise ValueError(f"规则 {rule_id} 不存在")
            
        if rule.status != "active":
            raise ValueError(f"规则 {rule_id} 未激活，无法执行")
            
        try:
            # 执行规则逻辑
            execution_result = await DecisionEngineService._execute_rule_logic(
                rule, input_data
            )
            
            execution_time = time.time() - start_time
            
            # 保存执行记录
            await DecisionExecution.create(
                id=execution_id,
                rule_id=rule_id,
                rule_name=rule.name,
                input_data=input_data,
                result=execution_result["result"],
                execution_path=execution_result["execution_path"],
                node_results=execution_result["node_results"],
                execution_time=execution_time,
                status=ExecutionStatus.COMPLETED.value
            )
            
            # 更新统计数据
            await DecisionEngineService._update_statistics(rule_id, True, execution_time)
            
            return {
                "rule_id": rule_id,
                "execution_id": execution_id,
                "result": execution_result["result"],
                "execution_path": execution_result["execution_path"],
                "node_results": execution_result["node_results"],
                "execution_time": execution_time,
                "created_at": datetime.now()
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # 保存错误记录
            await DecisionExecution.create(
                id=execution_id,
                rule_id=rule_id,
                rule_name=rule.name,
                input_data=input_data,
                result={},
                execution_path=[],
                node_results={},
                execution_time=execution_time,
                status=ExecutionStatus.FAILED.value,
                error_message=str(e)
            )
            
            # 更新统计数据
            await DecisionEngineService._update_statistics(rule_id, False, execution_time)
            
            raise e

    @staticmethod
    async def _execute_rule_logic(rule: DecisionRule, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行规则逻辑"""
        nodes = rule.nodes
        edges = rule.edges
        
        # 构建节点映射
        node_map = {node["id"]: node for node in nodes}
        
        # 构建边映射
        edge_map = {}
        for edge in edges:
            if edge["source"] not in edge_map:
                edge_map[edge["source"]] = []
            edge_map[edge["source"]].append(edge)
            
        # 找到开始节点
        start_nodes = [node for node in nodes if node["type"] == "data_source"]
        if not start_nodes:
            raise ValueError("没有找到开始节点")
            
        execution_path = []
        node_results = {}
        context = input_data.copy()
        
        # 从开始节点执行
        current_node = start_nodes[0]
        
        while current_node:
            node_id = current_node["id"]
            execution_path.append(node_id)
            
            # 执行当前节点
            node_result = await DecisionEngineService._execute_node(current_node, context)
            node_results[node_id] = node_result
            
            # 更新上下文
            if "output" in node_result:
                context.update(node_result["output"])
                
            # 决策节点是终点
            if current_node["type"] == "decision":
                break
                
            # 找到下一个节点
            next_node = None
            if node_id in edge_map:
                for edge in edge_map[node_id]:
                    # 根据节点类型和结果决定路径
                    if DecisionEngineService._should_follow_edge(current_node, node_result, edge):
                        next_node = node_map.get(edge["target"])
                        break
                        
            current_node = next_node
            
        # 生成最终结果
        final_result = DecisionEngineService._generate_final_result(node_results, context)
        
        return {
            "result": final_result,
            "execution_path": execution_path,
            "node_results": node_results
        }

    @staticmethod
    async def _execute_node(node: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个节点"""
        node_type = node["type"]
        node_data = node["data"]
        
        if node_type == "data_source":
            # 数据源节点：获取数据
            output_fields = node_data.get("outputFields", [])
            output = {field: context.get(field) for field in output_fields if field in context}
            return {"output": output}
            
        elif node_type == "condition":
            # 条件节点：评估条件
            condition = node_data.get("condition", "true")
            result = DecisionEngineService._evaluate_condition(condition, context)
            return {"result": result, "condition": condition}
            
        elif node_type == "model":
            # 模型节点：调用AI模型
            model_id = node_data.get("modelId")
            prediction = await DecisionEngineService._call_model(model_id, context)
            return {"prediction": prediction, "model_output": {"credit_risk": "low" if prediction > 0.7 else "high", "recommended_amount": int(prediction * 50000)}}
            
        elif node_type == "decision":
            # 决策节点：生成最终决策
            approval_condition = node_data.get("result", "false")
            max_amount = node_data.get("maxAmount", 50000)
            
            approved = DecisionEngineService._evaluate_condition(approval_condition, context)
            if approved:
                approved_amount = min(context.get("loanAmount", max_amount), max_amount)
                return {
                    "final_decision": "approved",
                    "approved_amount": approved_amount,
                    "risk_level": context.get("risk_level", "medium")
                }
            else:
                return {
                    "final_decision": "rejected",
                    "reason": "不满足审批条件"
                }
                
        elif node_type == "action":
            # 动作节点：执行特定动作
            action_type = node_data.get("actionType")
            if action_type == "calculate":
                formula = node_data.get("formula", "0")
                result = DecisionEngineService._evaluate_formula(formula, context)
                return {"calculation_result": result}
                
        return {}

    @staticmethod
    def _evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        try:
            # 替换变量
            eval_condition = condition
            for key, value in context.items():
                if isinstance(value, str):
                    eval_condition = eval_condition.replace(key, f"'{value}'")
                else:
                    eval_condition = eval_condition.replace(key, str(value))
                    
            # 替换操作符
            eval_condition = eval_condition.replace('&&', ' and ').replace('||', ' or ').replace('!', ' not ').replace('true', 'True').replace('false', 'False')
            
            # 安全评估
            allowed_names = {"__builtins__": {}, "True": True, "False": False, "None": None}
            return bool(eval(eval_condition, allowed_names))
        except:
            return False

    @staticmethod
    def _evaluate_formula(formula: str, context: Dict[str, Any]) -> float:
        """评估数学公式"""
        try:
            eval_formula = formula
            for key, value in context.items():
                if isinstance(value, (int, float)):
                    eval_formula = eval_formula.replace(key, str(value))
                    
            allowed_names = {"__builtins__": {}}
            return float(eval(eval_formula, allowed_names))
        except:
            return 0.0

    @staticmethod
    async def _call_model(model_id: str, context: Dict[str, Any]) -> float:
        """调用AI模型"""
        # 这里应该调用实际的AI模型
        # 目前返回模拟结果
        age = context.get("user.age", 25)
        income = context.get("user.income", 5000)
        credit = context.get("user.credit", 600)
        
        # 简单的评分逻辑
        score = 0.0
        if 18 <= age <= 65:
            score += 0.2
        if income > 5000:
            score += 0.3
        if credit > 700:
            score += 0.4
        elif credit > 600:
            score += 0.2
            
        # 添加随机因子
        import random
        score += random.uniform(-0.1, 0.1)
        
        return max(0.0, min(1.0, score))

    @staticmethod
    def _should_follow_edge(node: Dict[str, Any], node_result: Dict[str, Any], edge: Dict[str, Any]) -> bool:
        """判断是否应该沿着边走"""
        edge_type = edge.get("type", "default")
        
        if edge_type == "default":
            return True
        elif edge_type == "success":
            return node_result.get("result", False)
        elif edge_type == "failure":
            return not node_result.get("result", True)
            
        return True

    @staticmethod
    def _generate_final_result(node_results: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终结果"""
        # 找到决策节点的结果
        for node_id, result in node_results.items():
            if "final_decision" in result:
                decision_result = {
                    "decision": result["final_decision"],
                    "confidence": context.get("model_score", 0.5),
                    "risk_level": result.get("risk_level", "medium")
                }
                
                if result["final_decision"] == "approved":
                    decision_result["approved_amount"] = result.get("approved_amount", 0)
                else:
                    decision_result["reason"] = result.get("reason", "系统拒绝")
                    
                return decision_result
                
        # 默认结果
        return {
            "decision": "pending",
            "reason": "决策流程未完成"
        }

    @staticmethod
    async def test_rule(rule_id: str, test_cases: List[TestCase]) -> Dict[str, Any]:
        """测试规则"""
        total = len(test_cases)
        success = 0
        failure = 0
        results = []
        
        for test_case in test_cases:
            try:
                # 执行规则
                execution_result = await DecisionEngineService.execute_rule(
                    rule_id, test_case.input_data
                )
                
                # 检查结果是否匹配期望
                match_expected = DecisionEngineService._compare_results(
                    execution_result["result"], test_case.expected_result
                )
                
                if match_expected:
                    success += 1
                    status = "success"
                else:
                    failure += 1
                    status = "failure"
                    
                results.append({
                    "test_case": test_case.dict(),
                    "result": execution_result,
                    "status": status,
                    "match_expected": match_expected
                })
                
            except Exception as e:
                failure += 1
                results.append({
                    "test_case": test_case.dict(),
                    "result": {"error": str(e)},
                    "status": "failure",
                    "match_expected": False
                })
                
        return {
            "total": total,
            "success": success,
            "failure": failure,
            "success_rate": success / total if total > 0 else 0,
            "results": results
        }

    @staticmethod
    def _compare_results(actual: Dict[str, Any], expected: Dict[str, Any]) -> bool:
        """比较实际结果和期望结果"""
        for key, expected_value in expected.items():
            if key not in actual:
                return False
            if actual[key] != expected_value:
                return False
        return True

    @staticmethod
    async def get_execution_history(rule_id: Optional[str] = None, skip: int = 0, 
                                  limit: int = 100, start_date: Optional[date] = None,
                                  end_date: Optional[date] = None) -> Tuple[List[DecisionExecution], int]:
        """获取执行历史"""
        query = DecisionExecution.all()
        
        if rule_id:
            query = query.filter(rule_id=rule_id)
            
        if start_date:
            query = query.filter(created_at__gte=start_date)
            
        if end_date:
            query = query.filter(created_at__lte=end_date)
            
        total = await query.count()
        executions = await query.offset(skip).limit(limit).order_by('-created_at')
        
        return executions, total

    @staticmethod
    async def get_statistics() -> Dict[str, Any]:
        """获取统计数据"""
        # 规则统计
        total_rules = await DecisionRule.all().count()
        active_rules = await DecisionRule.filter(status="active").count()
        draft_rules = await DecisionRule.filter(status="draft").count()
        disabled_rules = await DecisionRule.filter(status="inactive").count()
        
        # 执行统计
        total_executions = await DecisionExecution.all().count()
        today_executions = await DecisionExecution.filter(
            created_at__gte=datetime.now().date()
        ).count()
        
        # 性能统计
        executions = await DecisionExecution.all().limit(1000)
        if executions:
            avg_execution_time = sum(e.execution_time for e in executions) / len(executions)
            success_count = sum(1 for e in executions if e.status == "completed")
            success_rate = success_count / len(executions)
        else:
            avg_execution_time = 0
            success_rate = 0
            
        # 最近执行
        recent_executions = await DecisionExecution.all().order_by('-created_at').limit(10)
        
        return {
            "total_rules": total_rules,
            "active_rules": active_rules,
            "draft_rules": draft_rules,
            "disabled_rules": disabled_rules,
            "total_executions": total_executions,
            "today_executions": today_executions,
            "avg_execution_time": avg_execution_time,
            "success_rate": success_rate,
            "rule_count": {
                "total": total_rules,
                "active": active_rules,
                "draft": draft_rules,
                "disabled": disabled_rules
            },
            "execution_stats": {
                "total": total_executions,
                "todayExecutions": today_executions,
                "last7Days": total_executions,  # 简化处理
                "last30Days": total_executions
            },
            "performance": {
                "avgResponseTime": avg_execution_time * 1000,  # 转换为毫秒
                "successRate": success_rate,
                "errorRate": 1 - success_rate
            },
            "recent_executions": [
                {
                    "id": e.id,
                    "rule_name": e.rule_name,
                    "result": e.result,
                    "execution_time": e.execution_time,
                    "created_at": e.created_at
                } for e in recent_executions
            ]
        }

    @staticmethod
    async def _update_statistics(rule_id: str, success: bool, execution_time: float):
        """更新统计数据"""
        today = datetime.now().date()
        
        # 更新规则统计
        stats, created = await DecisionStatistics.get_or_create(
            date=today,
            rule_id=rule_id,
            defaults={
                "total_executions": 0,
                "success_executions": 0,
                "failed_executions": 0,
                "avg_execution_time": 0.0
            }
        )
        
        stats.total_executions += 1
        if success:
            stats.success_executions += 1
        else:
            stats.failed_executions += 1
            
        # 更新平均执行时间
        stats.avg_execution_time = (
            (float(stats.avg_execution_time) * (stats.total_executions - 1) + execution_time) / 
            stats.total_executions
        )
        
        await stats.save()
        
        # 更新全局统计
        global_stats, created = await DecisionStatistics.get_or_create(
            date=today,
            rule_id=None,
            defaults={
                "total_executions": 0,
                "success_executions": 0,
                "failed_executions": 0,
                "avg_execution_time": 0.0
            }
        )
        
        global_stats.total_executions += 1
        if success:
            global_stats.success_executions += 1
        else:
            global_stats.failed_executions += 1
            
        global_stats.avg_execution_time = (
            (float(global_stats.avg_execution_time) * (global_stats.total_executions - 1) + execution_time) / 
            global_stats.total_executions
        )
        
        await global_stats.save()

    # 测试用例管理方法
    @staticmethod
    async def get_test_cases(skip: int = 0, limit: int = 100, 
                           keyword: Optional[str] = None) -> Tuple[List[DecisionTestCase], int]:
        """获取测试用例列表"""
        query = DecisionTestCase.all()
        
        if keyword:
            query = query.filter(
                Q(name__icontains=keyword) | 
                Q(description__icontains=keyword)
            )
            
        total = await query.count()
        test_cases = await query.offset(skip).limit(limit).order_by('-created_at')
        
        return test_cases, total

    @staticmethod
    async def create_test_case(test_case_data: TestCaseCreate) -> DecisionTestCase:
        """创建测试用例"""
        # 序列化输入数据
        serialized_input_data = DecisionEngineService._to_serializable(test_case_data.input_data)
        test_case = await DecisionTestCase.create(
            rule_id=test_case_data.rule_id,
            name=test_case_data.name,
            description=test_case_data.description,
            input_data=serialized_input_data,
            expected_result=test_case_data.expected_result
        )
        return test_case

    @staticmethod
    async def get_test_case(test_case_id: int) -> Optional[DecisionTestCase]:
        """获取测试用例详情"""
        return await DecisionTestCase.get_or_none(id=test_case_id)

    @staticmethod
    async def update_test_case(test_case_id: int, test_case_data: TestCaseUpdate) -> Optional[DecisionTestCase]:
        """更新测试用例"""
        test_case = await DecisionTestCase.get_or_none(id=test_case_id)

        if not test_case:
            return None
            
        # 序列化更新数据
        test_case.name = test_case_data.name
        test_case.description = test_case_data.description
        test_case.input_data = DecisionEngineService._to_serializable(test_case_data.input_data)
        test_case.expected_result = test_case_data.expected_result
        
        await test_case.save()
        return test_case

    @staticmethod
    async def delete_test_case(test_case_id: int) -> bool:
        """删除测试用例"""
        test_case = await DecisionTestCase.get_or_none(id=test_case_id)
        if not test_case:
            return False
            
        await test_case.delete()
        return True