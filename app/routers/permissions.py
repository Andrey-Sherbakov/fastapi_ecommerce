from fastapi import APIRouter
from starlette import status

from app.backend.db_depends import DbSessionDep
from app.helpers.auth import CurrUserPayloadDep, user_is_admin, get_user

router = APIRouter(prefix="/permission", tags=["permission"])


@router.patch("/supplier")
@user_is_admin
async def toggle_supplier_permission(
    db: DbSessionDep, curr_user: CurrUserPayloadDep, user_id: int
):
    user = await get_user(db, user_id)

    if user.is_supplier:
        user.is_supplier = False
        detail = "User is no longer supplier"
    else:
        user.is_supplier = True
        detail = "User is now supplier"

    await db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": detail}


@router.patch("/customer")
@user_is_admin
async def toggle_customer_permission(
    db: DbSessionDep, curr_user: CurrUserPayloadDep, user_id: int
):
    user = await get_user(db, user_id)

    if user.is_customer:
        user.is_customer = False
        detail = "User is no longer customer"
    else:
        user.is_customer = True
        detail = "User is now customer"

    await db.commit()
    return {"status_code": status.HTTP_200_OK, "detail": detail}


@router.delete("/delete")
@user_is_admin
async def delete_user(db: DbSessionDep, curr_user: CurrUserPayloadDep, user_id: int):
    user = await get_user(db, user_id)

    user.is_active = False
    await db.commit()

    return {"status_code": status.HTTP_200_OK, "detail": "User is deleted"}
