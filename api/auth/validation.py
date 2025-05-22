
from fastapi import Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from models import db_helper
from api.users.schemas import UserSchema
from api.users import crud
from fastapi.security import OAuth2PasswordBearer
from .jwt_tools import jwt_decode, check_pwd
from jwt import InvalidTokenError
from api.users.exceptions import UserNotFoundException
from .helpers import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_token_payload(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload: dict = jwt_decode(token)
        return payload
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )


def validate_token_type(payload: dict, token_type: str):
    type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(f"Invalid token type. Expected {token_type!r}, found {type!r}")
        )
    return True


async def get_current_user(
    session: AsyncSession,
    token_type: str,
    payload: dict,
) -> UserSchema:
    validate_token_type(
            payload=payload,
            token_type=token_type,
        )
    try:
        user = await crud.get_user_by_username(
            session=session,
            username=payload.get("sub"),
        )
        return user
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid"
        )


async def validate_user(
    username: str = Form(),
    password: str = Form(),
    session=Depends(db_helper.scoped_session_dependency),
) -> UserSchema:
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found!",
        )
    try:
        u = await crud.get_user_by_username(
            session=session,
            username=username)
    except UserNotFoundException:
        raise exception
    password_hash = u.password_hash
    if not check_pwd(password, password_hash):
        raise exception
    return u


async def get_user_for_access(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserSchema:
    u = await get_current_user(session, ACCESS_TOKEN_TYPE, payload)
    return u


async def get_user_for_refresh(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserSchema:
    u = await get_current_user(session, REFRESH_TOKEN_TYPE, payload)
    return u
