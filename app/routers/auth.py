from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert

from app.backend.db_depends import DbSessionDep
from app.helpers.auth import get_current_user_payload, authenticate_user, create_access_token, bcrypt_context
from app.models import User
from app.schemas import CreateUser

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
async def login(db: DbSessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db, form_data.username, form_data.password)

    token = await create_access_token(user.username, user.id, user.is_admin, user.is_supplier, user.is_customer,
                                      expires_delta=timedelta(minutes=20))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: DbSessionDep, new_user: CreateUser):
    await db.execute(insert(User).values(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        username=new_user.username,
        email=new_user.email,
        hashed_password=bcrypt_context.hash(new_user.password),
    ))

    await db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/read_current_user')
async def read_current_user(user: str = Depends(get_current_user_payload)):
    return {'User': user}
