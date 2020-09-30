#!./usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2020/9/29
# Author: Jimmy

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Item], summary="item列表")
def read_items(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve items.\n
    管理员可以查看所有人的item，普通用户只可以查看自己的item
    """
    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit)
    else:
        items = crud.item.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return items


@router.post("/", response_model=schemas.Item, summary="新增item")
def create_item(
        *,
        db: Session = Depends(deps.get_db),
        item_in: schemas.ItemCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new item.
    """
    item = crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return item


@router.put("/{pk}", response_model=schemas.Item, summary="更新item")
def update_item(
        *,
        db: Session = Depends(deps.get_db),
        pk: int,
        item_in: schemas.ItemUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an item.\n
    管理员可以更新所有人的item，普通用户只可以更新自己的item
    """
    item = crud.item.get(db=db, id=pk)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{pk}", response_model=schemas.Item, summary="item详情")
def read_item(
        *,
        db: Session = Depends(deps.get_db),
        pk: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.\n
    管理员可以获取所有人的item，普通用户只可以获取自己的item
    """
    item = crud.item.get(db=db, id=pk)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.delete("/{pk}", response_model=schemas.Item, summary="删除item")
def delete_item(
        *,
        db: Session = Depends(deps.get_db),
        pk: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.\n
    管理员可以删除所有人的item，普通用户只可以删除自己的item
    """
    item = crud.item.get(db=db, id=pk)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    item = crud.item.remove(db=db, pk=pk)
    return item
