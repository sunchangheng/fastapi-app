#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/11/2
# Author: Jimmy

"""
自定义响应封装
"""
from fastapi import HTTPException

APICODE = {
    1001: "成功",
    # 全局API错误码
    1002: "参数类型错误",
    1003: "缺少必传参数",
    1004: "参数长度错误",
    1005: "json数据格式有误",
    1006: "其他错误类型",
    1051: "token已过期",
    1052: "token无效",
    1053: "用户不存在",

    2001: "邮箱/密码不正确",
    2002: "用户未激活",
    2003: "当前用户没有足够的权限",

    2005: "用户已存在",
    2007: "Open user registration is forbidden on this server",
    2009: "The user doesn't have enough privileges",
    2010: "The user with this username does not exist in the system",

    3001: "Item not found",
    3003: "Not enough permissions"

}


class ErrorResponse(object):
    """失败的响应格式"""

    def __new__(cls, error_code, message=None, status_code=400):
        try:
            if message is None:
                message = APICODE[error_code]
        except KeyError:
            err = (
                "You use an undefined `code` without param `message` "
                "given!\nUse `code` define in class CodeMessage, or "
                "custom the `message` param."
            )
            raise Exception(err)

        result = {'status': error_code, 'message': message}

        return HTTPException(status_code=status_code, detail=result)


class StandardResponse(object):
    """成功的响应格式"""

    def __new__(cls, data, code=1001):
        result = {'status': code, 'data': data, 'message': APICODE[code]}
        return result


class PaginateResponse(object):
    """分页查询的响应格式"""

    def __new__(cls, page, size, total, pages, datas):
        data = {
            'page': page,
            'size': size,
            'total': total,
            'pages': pages,
            'items': datas
        }
        return StandardResponse(data)
