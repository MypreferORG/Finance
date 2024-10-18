# -*- coding: utf-8 -*-
"""
# @Create on : 2024/10/17 15:05
# @Author : Myprefer
# @Des: 支付功能服务
"""
from decimal import Decimal
import time
from config import settings
from alipay import AliPay


def alipay_obj():
    """
    生成支付alipay对象，以供调用
    :return: alipay 支付alipay对象
    """
    alipay = AliPay(
        appid=settings.ALIPAY_SETTING.get('ALIPAY_APP_ID'),
        app_notify_url=None,  # 默认回调 url
        app_private_key_string=open(settings.ALIPAY_SETTING.get('APP_PRIVATE_KEY_STRING')).read(),
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=open(settings.ALIPAY_SETTING.get('ALIPAY_PUBLIC_KEY_STRING')).read(),
        sign_type=settings.ALIPAY_SETTING.get('SIGN_TYPE'),  # RSA 或者 RSA2
        debug=settings.ALIPAY_SETTING.get('ALIPAY_DEBUG'),  # 默认 False
        verbose=False,  # 输出调试数据
        # config=AliPayConfig(timeout=50)  # 可选，请求超时时间
    )
    return alipay


def generate_payment_url(order_id: str, total_amount: Decimal, subject: str, return_url: str):
    """
    生成支付订单的支付宝URL
    :param order_id: 订单ID
    :param total_amount: 订单金额
    :param subject: 订单描述
    :param return_url: 支付成功后的回调URL
    :return: 支付订单的支付宝URL
    """
    # 获取alipay对象
    alipay = alipay_obj()

    # 生成支付订单URL
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,  # 商户订单号
        total_amount=str(total_amount),  # 订单总金额，必须是字符串
        subject=subject,  # 订单标题/描述
        return_url=return_url,  # 支付完成后的跳转URL
        notify_url=settings.ALIPAY_SETTING.get('ALIPAY_NOTIFY_URL')  # 支付宝服务器主动通知商户服务器里指定的页面http/https路径。
    )

    # 拼接完整的支付URL
    alipay_url = f"{settings.ALIPAY_SETTING.get('ALIPAY_GATEWAY_URL')}?{order_string}"

    return alipay_url


def verify_payment_result(data: dict):
    """
    验证支付宝支付结果
    :param data: 支付宝返回的数据
    :return: 验证结果，True 表示验证成功，False 表示验证失败
    """
    # 获取alipay对象
    alipay = alipay_obj()

    # 验证支付宝返回的数据是否合法
    success = alipay.verify(data, data.get("sign"))

    return success


def query_payment(order_id: str):
    """
    查询支付结果
    :param order_id: 商户订单号
    :return: 支付查询结果
    """
    # 获取alipay对象
    alipay = alipay_obj()

    # 查询支付结果
    result = alipay.api_alipay_trade_query(out_trade_no=order_id)

    if result.get("trade_status") == "TRADE_SUCCESS":
        return True
    else:
        return False

