from datetime import datetime
from decimal import Decimal

def model_to_description_dict(instance, keys_to_remove=None):
    model_class = type(instance)
    data = {}
    for field_name, field in model_class._meta.fields_map.items():
        if keys_to_remove and field_name in keys_to_remove:
            continue
        if not field.description:
            continue  # 跳过无描述的字段
        value = getattr(instance, field_name)
        if value is None or value == '':
            continue
        # 处理特殊类型
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, Decimal):
            value = float(value)
        elif isinstance(value, bool):
            value = '是' if value else '否'
        # 其他类型可继续补充（如 Decimal、UUID 等）
        data[field.description] = value
    return data


def model_to_raw_dict(instance, keys_to_remove=None):
    model_class = type(instance)
    data = {}
    for field_name, field in model_class._meta.fields_map.items():
        if keys_to_remove and field_name in keys_to_remove:
            continue
        value = getattr(instance, field_name)
        # 处理特殊类型
        if isinstance(value, datetime):
            value = value.strftime('%Y-%m-%d')
            # print(f"处理时间类型: {value}")
        elif isinstance(value, Decimal):
            value = float(value)
        # 其他类型可继续补充（如 Decimal、UUID 等）
        data[field.model_field_name] = value
    return data