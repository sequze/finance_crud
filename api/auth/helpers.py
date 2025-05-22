from .jwt_tools import jwt_encode
from datetime import timedelta
from config import settings
from api.users.schemas import UserSchema

TOKEN_TYPE_FIELD = "type"
REFRESH_TOKEN_TYPE = "refresh"
ACCESS_TOKEN_TYPE = "access"


def create_token(
    token_data: dict,
    token_type: str,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return jwt_encode(
        jwt_payload,
        expire_timedelta=expire_timedelta,
    )


def create_refresh_token(user: UserSchema):
    payload = {
        "sub": user.username,
    }
    return create_token(
        payload, REFRESH_TOKEN_TYPE, timedelta(days=settings.jwt_settings.refresh_token_expire_days)
    )


def create_access_token(user: UserSchema):
    payload = {
        "sub": user.username,
        "username": user.username,
        "balance": user.balance,
    }
    return create_token(payload, ACCESS_TOKEN_TYPE)
