#!./usr/bin/env python3
# -*- coding: utf-8 -*-
# Date: 2021/8/23
# Author: sunchangheng
"""
自定义响应封装
"""

from fastapi import HTTPException

api_code = {
    # 全局API错误码
    1002: "参数类型错误",
    1003: "缺少必传参数",
    1004: "参数长度错误",
    1005: "json数据格式有误",
    1006: "其他错误类型",
    1051: "登录凭证已过期, 请重新登录",
    1052: "Token无效",
    1053: "用户不存在",
    1055: "Token为空",
    1057: "密码错误",

    # 其他异常
    -1: "",
}


class ErrorResponse(HTTPException):
    """失败的响应格式"""

    def __new__(cls, error_code, message=None, data=(), status_code=200):
        if type(error_code) is str:
            result = {"code": -1, "msg": error_code, "data": data}
            return HTTPException(status_code=status_code, detail=result)

        try:
            if message is None:
                message = api_code[error_code]
        except KeyError:
            err = (
                "You use an undefined `code` without param `message` "
                "given!\nUse `code` define in class CodeMessage, or "
                "custom the `message` param."
            )
            raise Exception(err)

        result = {"code": error_code, "msg": message, "data": data}

        return HTTPException(status_code=status_code, detail=result)


class StandardResponse(object):
    """成功的响应格式"""

    def __new__(cls, data=(), msg="success"):
        result = {"code": 0, "data": data, "msg": msg}
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
