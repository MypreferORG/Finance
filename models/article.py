# -*- coding: utf-8 -*-
"""
# @Create on : 10/7/24 9:30 PM
# @Author : Myprefer
# @Des: 文章及公告模型
"""

from tortoise import fields
from tortoise.models import Model


class Article(Model):
    """
    文章表：用于记录微信公众号文章的信息
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, description="文章标题")
    content = fields.TextField(description="文章内容，支持Markdown或HTML格式")
    author = fields.CharField(max_length=100, description="作者姓名或昵称")
    publish_date = fields.DatetimeField(auto_now_add=True, description="文章发布时间")
    updated_at = fields.DatetimeField(auto_now=True, description="文章最后更新时间")
    status = fields.CharField(max_length=20, default="published", description="文章状态（如：published、hidden、deleted等）")
    cover_image = fields.CharField(max_length=255, null=True, description="封面图片URL")
    summary = fields.TextField(null=True, description="文章摘要或简介")
    views = fields.IntField(default=0, description="阅读次数")

    class Meta:
        table = "article"
        indexes = [("title", "publish_date")]  # 根据标题和发布时间创建索引

    def __str__(self):
        return f"Article(id={self.id}, title={self.title}, author={self.author}, status={self.status})"


class Announcement(Model):
    """
    公告表：用于记录系统公告和通知的信息
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255, description="公告标题")
    content = fields.TextField(description="公告内容，支持Markdown或HTML格式")
    publish_date = fields.DatetimeField(auto_now_add=True, description="公告发布时间")
    updated_at = fields.DatetimeField(auto_now=True, description="公告最后更新时间")
    status = fields.CharField(max_length=20, default="active", description="公告状态（如：active、inactive、archived等）")
    author = fields.CharField(max_length=100, null=True, description="公告发布者姓名或昵称")
    expiration_date = fields.DatetimeField(null=True, description="公告过期时间（可选）")

    class Meta:
        table = "announcement"
        indexes = [("title", "publish_date")]  # 根据标题和发布时间创建索引

    def __str__(self):
        return f"Announcement(id={self.id}, title={self.title}, author={self.author}, status={self.status})"