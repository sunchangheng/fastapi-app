#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy
import os
import secrets
from typing import Union, Optional, List
from pydantic import AnyHttpUrl, BaseSettings, IPvAnyAddress


class TestConfig(BaseSettings):
    """
    测试环境配置
    """
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "yo5mCDHCnhOtyI60GPmuolPVYvX9pQzQQ1kdMwWMqcM"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # MySQL配置
    MYSQL_USERNAME: str = 'root'
    MYSQL_PASSWORD: str = "123456"
    MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = "127.0.0.1"
    MYSQL_DATABASE: str = 'face_api'

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"

    USERS_OPEN_REGISTRATION = True  # 是否开方注册 （True 开放）（False 未开放）


# class ProConfig(BaseSettings):
#     """
#     生产环境配置
#     """
#     # 文档地址 成产环境可以关闭 None
#     DOCS_URL: Optional[str] = "/api/v1/docs"
#     # # 文档关联请求数据接口 成产环境可以关闭 None
#     OPENAPI_URL: Optional[str] = "/api/v1/openapi.json"
#     # 禁用 redoc 文档
#     REDOC_URL: Optional[str] = None
#
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 天
#     SECRET_KEY: str = '-*&^)()sd(*A%&^aWEQaasda_asdasd*&*)(asd%$#'
#
#     MYSQL_USERNAME: str = os.getenv("MYSQL_USER", "root")
#     MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "admin")
#     MYSQL_HOST: Union[AnyHttpUrl, IPvAnyAddress] = os.getenv("MYSQL_HOST", "127.0.0.1")
#     MYSQL_DATABASE: str = 'Mall'
#
#     # Mysql地址
#     SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@" \
#                               f"{MYSQL_HOST}/{MYSQL_DATABASE}?charset=utf8mb4"


settings = TestConfig()
