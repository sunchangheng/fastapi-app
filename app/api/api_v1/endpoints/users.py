#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy
from typing import Any

from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.services.response import StandardResponse, ErrorResponse

router = APIRouter()


@router.get("/", summary="用户列表（管理员）")
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)

    return StandardResponse(users)


@router.post("/", summary="创建用户（管理员）")
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    创建用户（管理员权限可操作）
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise ErrorResponse(2005)

    user = crud.user.create(db, obj_in=user_in)

    return StandardResponse(user)


@router.put("/me", summary="更新当前用户信息")
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        full_name: str = Body(None),
        email: EmailStr = Body(None),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    更新当前用户信息
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)

    return StandardResponse(user)


@router.get("/me", summary="查看当前用户信息")
def read_user_me(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return StandardResponse(current_user)


@router.post("/open", summary="注册用户")
def create_user_open(
        *,
        db: Session = Depends(deps.get_db),
        email: EmailStr = Body(...),
        password: str = Body(...),
        full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise ErrorResponse(2007, status_code=403)
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise ErrorResponse(2005)
    user_in = schemas.UserCreate(password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)

    return StandardResponse(user)


@router.get("/{user_id}", summary="用户详情（管理员）")
def read_user_by_id(
        user_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise ErrorResponse(2009)

    return StandardResponse(user)


@router.put("/{user_id}", summary="修改用户信息（管理员）")
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise ErrorResponse(2010, status_code=404)

    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    return StandardResponse(user)
