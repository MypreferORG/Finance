# -*- coding: utf-8 -*-
"""
短信风控服务
集成 message_retrieval.py 的风控识别功能
"""

from typing import List, Dict, Any
from utils.message_retrieval import comprehensive_risk_analysis
import logging

logger = logging.getLogger(__name__)


class SmsRiskService:
    """短信风控服务类"""
    
    @staticmethod
    def analyze_sms_risk(sms_list: List[Dict[str, Any]], device_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        分析短信风险
        
        Args:
            sms_list: 短信列表，格式为 [{"telphone": "", "content": "", "type": "", "sendDate": ""}]
            device_info: 设备信息（可选）
            
        Returns:
            风控分析结果
        """
        try:
            # 记录请求信息
            logger.info(f"开始分析短信风险，短信数量: {len(sms_list)}")
            
            if device_info:
                logger.info(f"设备信息: {device_info}")
            
            # 调用风控分析引擎
            risk_result = comprehensive_risk_analysis(sms_list)
            
            # 记录分析结果
            logger.info(f"风控分析完成，决策: {risk_result.get('final_decision', 'UNKNOWN')}")
            
            return risk_result
            
        except Exception as e:
            logger.error(f"短信风控分析异常: {str(e)}", exc_info=True)
            return {
                "final_decision": "ERROR",
                "error": str(e),
                "analysis_summary": "系统异常，请稍后重试"
            }
    
    @staticmethod
    def format_response(risk_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化响应结果
        
        Args:
            risk_result: 原始风控结果
            
        Returns:
            格式化后的响应数据
        """
        # 提取关键信息
        decision = risk_result.get("final_decision", "UNKNOWN")
        risk_tags = risk_result.get("risk_tags", [])
        summary = risk_result.get("analysis_summary", "")
        risk_count = risk_result.get("raw_risk_count", 0)
        error = risk_result.get("error")
        
        response = {
            "final_decision": decision,
            "risk_count": risk_count,
            "summary": summary
        }
        
        if risk_tags:
            response["risk_tags"] = risk_tags
        
        if error:
            response["error"] = error
            
        # 添加风险等级说明
        risk_level_map = {
            "PASS": "低风险",
            "LOWER_SCORE": "降低评分",
            "LOWER_LIMIT": "降低额度",
            "MANUAL_REVIEW": "人工审核",
            "REJECT": "拒绝",
            "ERROR": "系统异常"
        }
        
        response["risk_level"] = risk_level_map.get(decision, "未知")
        
        return response
