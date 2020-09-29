#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy

from fastapi import APIRouter

from app.api.api_v1.endpoints import users, items, login

api_v1_router = APIRouter()


api_v1_router.include_router(login.router, tags=["login"])
api_v1_router.include_router(users.router, prefix="/users", tags=["users"])
api_v1_router.include_router(items.router, prefix="/items", tags=["items"])
