# -*- coding: utf-8 -*-
"""
# @Create on : 2024/11/24 22:03
# @Author : Myprefer
# @Des: 身份证验证服务
"""
import json
import os
import re
from fastapi import UploadFile, HTTPException
import aiohttp
from config import settings
from alibabacloud_ocr_api20210707.client import Client as ocr_api20210707Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_darabonba_stream.client import Client as StreamClient
from alibabacloud_ocr_api20210707 import models as ocr_api_20210707_models
from alibabacloud_tea_util import models as util_models


def is_valid_id_card(id_card_number: str) -> bool:
    """
    验证身份证号码格式（支持中国大陆二代身份证）
    :param id_card_number: 身份证号码
    :return: 是否有效
    """
    id_card_pattern = r"^[0-9]{17}[0-9xX]$"
    return re.match(id_card_pattern, id_card_number) is not None


# 调用 OCR 微服务
async def verify_id_card_photo(file: UploadFile, side: str,
                               full_name: str, id_card_number: str):
    """
    调用 OCR 微服务验证身份证照片内容。
    :param id_card_number:
    :param full_name:
    :param file: 上传的身份证照片
    :param side: "front" 表示正面，"back" 表示反面
    :return: OCR 返回的解析结果
    """
    service_url = settings.OCR_URL  # 你的 OCR 微服务地址
    try:
        # 创建一个 FormData 对象并添加文件
        form_data = aiohttp.FormData()
        form_data.add_field(
            "pic",  # 该字段名需要与服务端的字段名一致
            await file.read(),  # 读取文件内容
            filename=file.filename,
            content_type=file.content_type,
        )
        # form_data.add_field("side", side)  # 添加额外的字段（如身份证正反面）

        # 发送异步请求
        async with aiohttp.ClientSession() as session:
            async with session.post(service_url, data=form_data) as response:
                if response.status != 200:
                    raise HTTPException(status_code=response.status, detail="OCR 微服务调用失败")
                result = await response.json()  # 解析 JSON 响应
                # 验证身份证号码和姓名是否匹配
                if result.get("idnum") != id_card_number or result.get("name") != full_name:
                    raise HTTPException(status_code=400, detail="身份证信息不匹配")
                return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR 服务错误: {str(e)}")


# 比对身份证信息
def verify_idcard_details(front_info, back_info, idcard_details: dict) -> bool:
    """
    比对身份证正反面信息
    :param front_info: 身份证正面信息
    :param back_info: 身份证反面信息
    :param idcard_details: 用户填写的身份证信息
    :return: 是否一致
    """
    # 先提取身份证信息
    front_data = json.loads(front_info.body.data)
    front_data = front_data.get("data").get("face").get("data")

    back_data = json.loads(back_info.body.data)
    back_data = back_data.get("data").get("back").get("data")
    id_card_expiry = back_data.get("validPeriod").split('-')[1].replace('.', '-')

    if front_data.get("name") != idcard_details.get("name"):
        return False
    if front_data.get("idNumber") != idcard_details.get("idNumber"):
        return False
    if str(idcard_details.get("id_card_expiry")) != id_card_expiry:
        return False
    return True


async def create_client() -> ocr_api20210707Client:
    """
    使用AK&SK初始化账号Client
    @return: Client
    @throws Exception
    """
    # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
    # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
    config = open_api_models.Config(
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。
        access_key_id=os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'],
        # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        access_key_secret=os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
    )
    # Endpoint 请参考 https://api.aliyun.com/product/ocr-api
    config.endpoint = f'ocr-api.cn-hangzhou.aliyuncs.com'
    return ocr_api20210707Client(config)


# 调用第三方实名认证服务
async def verify_identity_with_third_party(front_path, back_path, idcard_details: dict):
    """
    调用第三方实名认证服务验证身份证信息
    :param front_path: 身份证正面照片路径
    :param back_path: 身份证反面照片路径
    :param idcard_details: 身份证信息
    :return: 是否验证通过
    """
    client = await create_client()
    # 需要安装额外的依赖库，直接点击下载完整工程即可看到所有依赖。
    front_stream = StreamClient.read_from_file_path(front_path)
    back_stream = StreamClient.read_from_file_path(back_path)
    front_recognize_idcard_request = ocr_api_20210707_models.RecognizeIdcardRequest(
        output_quality_info=False,
        output_figure=False,
        body=front_stream
    )
    back_recognize_idcard_request = ocr_api_20210707_models.RecognizeIdcardRequest(
        output_quality_info=False,
        output_figure=False,
        body=back_stream
    )
    runtime = util_models.RuntimeOptions()
    try:
        # 复制代码运行请自行打印 API 的返回值
        front_result = client.recognize_idcard_with_options(front_recognize_idcard_request, runtime)
        back_result = client.recognize_idcard_with_options(back_recognize_idcard_request, runtime)
        # 从返回结果中提取身份证信息，比对用户填写的信息，包括姓名、身份证号码和有效期
        if verify_idcard_details(front_result, back_result, idcard_details):
            return True
    except Exception as error:
        # 此处仅做打印展示，请谨慎对待异常处理，在工程项目中切勿直接忽略异常。
        # 错误 message
        print(error)
    return False
