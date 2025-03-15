# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/15 17:27
# @Author : Myprefer
# @Des: 
"""
import os
import random
from datetime import timedelta
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
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


# async def send_sms_code_message(
#         sms_tips: tuple,
#         sms_template_id: str = settings.RL_SMS_TEMPLATE_ID,
#         receive_mobile: str = settings.RL_TEST_MOBILE
# ):
#     """
#     发送短信验证码
#     :param sms_tips: 验证码提示信息 eg: (验证码, 有效期) 有效期单位是分钟
#     :param sms_template_id: 短信模板id
#     :param receive_mobile: 接受的手机号
#     :return:
#     """
#     sdk = SmsSDK(settings.RL_ACCID, settings.RL_ACCTOKEN, settings.RL_APPID)
#     sms_resp_json_str = sdk.sendMessage(sms_template_id, receive_mobile, sms_tips)
#     sms_resp_dict = json.loads(sms_resp_json_str)
#     print(sms_resp_dict)
#     if sms_resp_dict.get('statusCode') == '000000':
#         # 发送成功
#         return True
#     else:
#         return False


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
    success = await send_sms_code_message(mobile, sms_code)

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


def create_client() -> Dysmsapi20170525Client:
    """
    使用AK&SK初始化账号Client
    @return: Client
    @throws Exception
    """
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
    # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
    config = open_api_models.Config(
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
        access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
        access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
    )
    # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
    config.endpoint = f'dysmsapi.aliyuncs.com'
    return Dysmsapi20170525Client(config)


async def send_sms_code_message(phone_number: str,code: str):
    client = create_client()
    send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
        phone_numbers=phone_number,
        sign_name='启航',
        template_code='SMS_478435081',
        template_param=f'{{"code":"{code}"}}'
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        await client.send_sms_with_options_async(send_sms_request, runtime)
        return True
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error.message)
        # 诊断地址
        print(error.data.get("Recommend"))
        UtilClient.assert_as_string(error.message)
        return False
