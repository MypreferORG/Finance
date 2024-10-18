# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/15 17:27
# @Author : Myprefer
# @Des: 
"""
import json
import random
from datetime import timedelta

from ronglian_sms_sdk import SmsSDK
from config import settings
from db.redis import sys_cache


def generate_sms_code():
    """
    随机生成6位短信验证码
    :return: sms_code
    """
    # 随机6位短信验证码
    sms_code = random.randint(100000, 999999)
    sms_code = list(str(sms_code))
    random.shuffle(sms_code)
    sms_code = ''.join(sms_code)
    return sms_code


async def send_sms_code_message(
        sms_tips: tuple,
        sms_template_id: str = settings.RL_SMS_TEMPLATE_ID,
        receive_mobile: str = settings.RL_TEST_MOBILE
):
    """
    发送短信验证码
    :param sms_tips: 验证码提示信息 eg: (验证码, 有效期) 有效期单位是分钟
    :param sms_template_id: 短信模板id
    :param receive_mobile: 接受的手机号
    :return:
    """
    sdk = SmsSDK(settings.RL_ACCID, settings.RL_ACCTOKEN, settings.RL_APPID)
    sms_resp_json_str = sdk.sendMessage(sms_template_id, receive_mobile, sms_tips)
    sms_resp_dict = json.loads(sms_resp_json_str)
    print(sms_resp_dict)
    if sms_resp_dict.get('statusCode') == '000000':
        # 发送成功
        return True
    else:
        return False


# def main():
#     sms_code = generate_sms_code()
#     sms_tips = (sms_code, settings.sms_code_ttl)
#     send_sms_code_message(sms_tips)
#
#
# if __name__ == '__main__':
#     main()


async def generate_and_send_code(mobile: str):
    """
    生成验证码并发送短信，同时将验证码存储到Redis
    :param mobile: 接收验证码的手机号
    :return: 是否发送成功
    """
    # 生成6位验证码
    sms_code = generate_sms_code()

    # 发送验证码
    success = await send_sms_code_message(sms_tips=(sms_code, '5'), receive_mobile=mobile)

    if success:
        # 验证码发送成功，将验证码存储到 Redis，有效期5分钟
        cache = await sys_cache()
        await cache.set(f"sms_code:{mobile}", sms_code, ex=timedelta(minutes=5))
        return True
    else:
        return False


async def verify_sms_code(mobile: str, code: str) -> bool:
    """
    验证用户输入的验证码
    :param mobile: 用户手机号
    :param code: 用户输入的验证码
    :return: 验证结果，True表示成功，False表示失败
    """
    cache = await sys_cache()
    stored_code = await cache.get(f"sms_code:{mobile}")

    if stored_code is None:
        # 验证码不存在或已过期
        return False

    if stored_code == code:
        # 验证成功，删除 Redis 中的验证码
        await cache.delete(f"sms_code:{mobile}")
        return True
    else:
        # 验证码不匹配
        return False