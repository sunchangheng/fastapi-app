from typing import Generator

import jose
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session

from app import crud, models
from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import SessionLocal
from app.services.response import ErrorResponse

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # noqa


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> models.User:
    """
    获取当前登录用户
    :param db:
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')

    except jose.exceptions.ExpiredSignatureError:
        raise ErrorResponse(1051)

    except jose.exceptions.JWTError:
        raise ErrorResponse(1052)

    user = crud.user.get(db, id=user_id)
    if not user:
        raise ErrorResponse(1053)

    return user


def get_current_active_user(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    验证是否是已激活的用户
    """
    if not crud.user.is_active(current_user):
        raise ErrorResponse(2002)
    return current_user


def get_current_active_superuser(
        current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    验证是否是超级管理员
    """
    if not crud.user.is_superuser(current_user):
        raise ErrorResponse(2003)
    return current_user
