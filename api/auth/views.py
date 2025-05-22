from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from .helpers import (
    ACCESS_TOKEN_TYPE,
    create_access_token,
    create_refresh_token,
    REFRESH_TOKEN_TYPE,
)
from api.users.schemas import UserSchema
from pydantic import BaseModel
from .validation import (
    validate_token_type,
    validate_user,
    get_token_payload,
    get_user_for_access,
    get_user_for_refresh,
)

bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/auth", tags=["Auth"], dependencies=[Depends(bearer)])


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str | None = None


@router.post("/login", response_model=TokenInfo)
def login(
    user: UserSchema = Depends(validate_user),
) -> TokenInfo:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
        refresh_token=refresh_token,
    )


@router.get("/users/me")
def user_info(
    payload: dict = Depends(get_token_payload),
    user: UserSchema = Depends(get_user_for_access),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "balance": user.balance,
        "logged_in": iat,
    }


@router.post(
    "/refresh", 
    response_model=TokenInfo, 
    response_model_exclude_none=True)
def refresh(user: UserSchema = Depends(get_user_for_refresh)) -> TokenInfo:
    return TokenInfo(access_token=create_access_token(user))