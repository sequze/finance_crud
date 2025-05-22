import jwt
import bcrypt
from config import settings
from datetime import datetime, timedelta, timezone


def jwt_encode(
    payload: dict,
    expire_timedelta: timedelta | None = None,
    private_key: str = settings.jwt_settings.private_key_path.read_text(),
    algorithm: str = settings.jwt_settings.algorithm,
    expire_minutes: int = settings.jwt_settings.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        exp = now + expire_timedelta
    else:
        exp = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=exp,
        iat=now,
    )
    return jwt.encode(to_encode, private_key, algorithm=algorithm)


def jwt_decode(
    token: str | bytes,
    public_key: str = settings.jwt_settings.public_key_path.read_text(),
    algorithm: str = settings.jwt_settings.algorithm,
):
    return jwt.decode(token, public_key, algorithms=[algorithm])


def hash_pwd(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_pwd(
    password: str,
    password_hash: bytes,
):
    return bcrypt.checkpw(password.encode(), password_hash)
