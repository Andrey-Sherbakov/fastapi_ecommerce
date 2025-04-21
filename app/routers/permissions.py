from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.backend.db_depends import get_db
from app.helpers.auth import validate_user_is_admin, validate_user_is_active
from app.models.user import User
from app.routers.auth import get_current_user_payload

router = APIRouter(prefix='/permission', tags=['permission'])


@router.patch('/supplier')
async def toggle_supplier_permission(db: Annotated[AsyncSession, Depends(get_db)],
                                     current_user: Annotated[dict, Depends(get_current_user_payload)], user_id: int):
    validate_user_is_admin(current_user)

    user = await db.scalar(select(User).where(User.id == user_id))

    validate_user_is_active(user)

    if user.is_supplier:
        user.is_supplier = False
        detail = 'User is no longer supplier'
    else:
        user.is_supplier = True
        detail = 'User is now supplier'

    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'detail': detail
    }


@router.patch('/customer')
async def toggle_customer_permission(db: Annotated[AsyncSession, Depends(get_db)],
                                     user_payload: Annotated[dict, Depends(get_current_user_payload)], user_id: int):
    validate_user_is_admin(user_payload)

    user = await db.scalar(select(User).where(User.id == user_id))

    validate_user_is_active(user)

    if user.is_customer:
        user.is_customer = False
        detail = 'User is no longer customer'
    else:
        user.is_customer = True
        detail = 'User is now customer'

    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'detail': detail
    }


@router.delete('/delete')
async def delete_user(db: Annotated[AsyncSession, Depends(get_db)],
                      user_payload: Annotated[dict, Depends(get_current_user_payload)], user_id: int):
    validate_user_is_admin(user_payload)

    user = await db.scalar(select(User).where(User.id == user_id))

    validate_user_is_active(user)

    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete admin user"
        )

    user.is_active = False
    await db.commit()

    return {
        'status_code': status.HTTP_200_OK,
        'detail': 'User is deleted'
    }
