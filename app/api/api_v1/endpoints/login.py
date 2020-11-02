#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services.response import ErrorResponse, StandardResponse

router = APIRouter()


@router.post("/login/access-token", summary="登录")
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise ErrorResponse(2001)
    elif not crud.user.is_active(user):
        raise ErrorResponse(2002)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }
    return StandardResponse(data)


@router.post("/login/test-token", summary="验证Token是否有效")
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    data = jsonable_encoder(current_user)
    data.pop('hashed_password')
    return StandardResponse(data)
