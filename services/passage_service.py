# -*- coding: utf-8 -*-
"""
# @Create on : 2025/3/13 21:30
# @Author : Myprefer
# @Des: 个性化文章推荐
"""

# 依赖关系：
# search_articles_by_keywords -> get_recommend_articles
# -> get_user_info -> model_to_description_dict
import time
import json
import re
from http import HTTPStatus
from dashscope import Application
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
from utils.model2dict import model_to_description_dict


def get_user_info(user_profile, user_application, user_behavior):
    """
    获取用户信息
    :param user_id:
    :return:
    """
    user_info = {}

    # user_profile = dict(user_profile)
    # user_application = dict(user_application)
    # user_behavior = dict(user_behavior)

    keys_to_remove = [
        'id', 'user_id', 'created_at', 'updated_at', 'user', 'username',
        'full_name', 'phone_number', 'id_card_number', 'id_card_expiry',
        'bank_account', 'date_of_birth', 'profile_picture', 'is_profile_completed'
    ]

    # 移除无关字段
    # if user_profile:
    #     for key in keys_to_remove:
    #         user_profile.pop(key, None)
    # if user_application:
    #     for key in keys_to_remove:
    #         user_application.pop(key, None)
    # if user_behavior:
    #     for key in keys_to_remove:
    #         user_behavior.pop(key, None)

    # 合并所有模型的数据
    if user_profile:
        user_info.update(model_to_description_dict(user_profile, keys_to_remove))
    if user_application:
        user_info.update(model_to_description_dict(user_application, keys_to_remove))
    if user_behavior:
        user_info.update(model_to_description_dict(user_behavior, keys_to_remove))


    return json.dumps(user_info, ensure_ascii=False)


def get_recommend_articles(user_info):
    """
    :param user_info:
    :return: list:推荐关键词列表
    """
    # 默认关键词
    default_keywords = [
        "贷款申请流程",
        "如何提高信用评分",
        "贷款利率计算",
        "提前还款的利弊",
        "如何选择贷款产品",
        "信用报告解读",
        "贷款逾期处理",
        "理财基础知识",
        "如何规划个人财务",
    ]

    print(f'用户信息：{user_info}')
    try:
        response = Application.call(
            api_key='sk-ba60782b21b2488285776a2dcb340cc1',
            app_id='6691e60b12544acaac0a0bd0416f8864',
            prompt=user_info
        )

        if response.status_code != HTTPStatus.OK:
            print(f"API 调用失败: {response.message}")
            return default_keywords  # 返回默认关键词

        # 解析 API 响应，提取推荐关键词
        json_pattern = r"```json\n([\s\S]*?)\n```"
        match = re.search(json_pattern, response.output.text)
        if match:
            search_keywords = match.group(1).strip().replace('\n', '')
            search_keywords = json.loads(search_keywords)
            print(f"推荐关键词: {search_keywords}")
            articlas = search_articles_by_keywords(search_keywords['keywords'])
            return articlas
        else:
            articlas = search_articles_by_keywords(default_keywords)
            return  articlas # 返回默认关键词
    except Exception as e:
        print(f"API 调用异常: {e}")
        articlas = search_articles_by_keywords(default_keywords)
        return articlas  # 返回默认关键词


def search_articles_by_keywords(keywords):
    """
    根据关键词列表搜索文章，并返回文章名、摘要和链接。

    :param keywords: list, 关键词列表
    :return: list of dict, 包含文章名、摘要和链接的字典列表
    """
    search_results = []
    ddgs = DDGS()  # 创建 DDGS 实例
    for keyword in keywords:
        try:
            results = ddgs.text(keyword, max_results=1)  # 每个关键词返回 3 条结果
            for result in results:
                search_results.append({
                    "title": result.get("title", "无标题"),
                    "summary": result.get("body", "略"),  # 如果没有摘要，则用 "略" 代替
                    "url": result.get("href", "无链接")
                })
            time.sleep(2)  # 每次请求后等待 2 秒，避免触发速率限制
        except DuckDuckGoSearchException as e:
            print(f"搜索关键词 '{keyword}' 时出错: {e}")
            time.sleep(5)  # 如果出错，等待 5 秒后继续
    return search_results