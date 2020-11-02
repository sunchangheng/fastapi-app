#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy

import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.routers import api_v1_router
from app.core.config import settings


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # application.include_router(api_v1_router)
    application.include_router(api_v1_router, prefix=settings.API_V1_STR)

    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """计算API响应时间的中间件"""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        """
        请求异常拦截器
        :param request:
        :param exc:
        :return:
        """
        errors = exc.errors()

        error_type = errors[0].get('type')
        loc = errors[0].get('loc')

        temp = error_type.split('.')[0]
        if temp == 'type_error':
            try:
                error_arg = loc[1]
            except IndexError:
                error_arg = ''

            status = 1002
            message = f'参数类型错误: {error_arg}'

        elif error_type == 'value_error.missing':
            status = 1003
            print('loc', loc)
            try:
                message = f'缺少必传参数: {loc[1]}'
            except IndexError:
                message = f'缺少必传参数'

        elif error_type in [
            'value_error.any_str.max_length',
            'value_error.any_str.min_length'
        ]:
            status = 1004
            message = f'参数长度错误: {loc[1]}'

        elif error_type == 'value_error.jsondecode':
            status = 1005
            message = f'json数据格式有误：{loc[1]}'

        else:
            status = 1006
            message = f'其他错误类型：\n {str(exc)}'

        return JSONResponse(status_code=200, content={'status': status, 'message': message})

    @application.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request, exc):
        """响应异常拦截器"""
        headers = getattr(exc, "headers", None)
        if headers:
            return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=headers)
        else:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return application


app = get_application()

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True, debug=True)
