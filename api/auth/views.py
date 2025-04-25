from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .jwt_tools import check_pwd, jwt_encode, jwt_decode
from models import db_helper, User
from pydantic import BaseModel
from api.users import crud
from api.users.exceptions import UserNotFoundException
from jwt.exceptions import InvalidTokenError

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class TokenInfo(BaseModel):
    access_token: str
    token_type: str



async def validate_user(
    username: str = Form(),
    password: str = Form(),
    session=Depends(db_helper.scoped_session_dependency),
) -> User:
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


@router.post("/login", response_model=TokenInfo)
def login(
    user: User = Depends(validate_user),
) -> TokenInfo:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "balance": user.balance,
    }
    token = jwt_encode(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


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

async def get_current_user(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> User:
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



@router.get("/users/me")
def user_info(
    payload: dict = Depends(get_token_payload),
    user: User = Depends(get_current_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "balance": user.balance,
        "logged_in": iat,
    }
