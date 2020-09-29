#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", summary="所有用户")
async def read_users():
    return [{"username": "Foo"}, {"username": "Bar"}]


@router.get("/users/me", summary="个人信息")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", summary="用户信息")
async def read_user(username: str):
    return {"username": username}
