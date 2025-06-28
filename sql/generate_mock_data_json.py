# -*- coding: utf-8 -*-
"""
# @Create on : 2024/07/11
# @Author : AI Assistant
# @Des: 生成模拟数据并保存为JSON文件
"""

import json
import os
from datetime import datetime
from decimal import Decimal
from mock_data import generate_all_mock_data

# 自定义JSON编码器，处理Decimal和datetime类型
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        return super().default(obj)

def save_mock_data_to_json():
    """生成模拟数据并保存为JSON文件"""
    print("正在生成模拟数据...")
    mock_data = generate_all_mock_data()
    
    # 创建输出目录
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mock_data_json")
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存完整数据
    full_data_path = os.path.join(output_dir, "full_mock_data.json")
    with open(full_data_path, "w", encoding="utf-8") as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)
    print(f"完整模拟数据已保存至: {full_data_path}")
    
    # 分别保存各类数据
    for data_type, data_list in mock_data.items():
        file_path = os.path.join(output_dir, f"{data_type}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)
        print(f"{data_type} 数据已保存至: {file_path}")
    
    print("所有模拟数据已成功保存为JSON文件！")

if __name__ == "__main__":
    save_mock_data_to_json()