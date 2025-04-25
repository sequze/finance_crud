from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).parent


class JwtSettings(BaseModel):
    private_key_path: Path
    public_key_path: Path
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/finance.db"
    db_echo: bool = True
    jwt_settings: JwtSettings = JwtSettings(
        private_key_path=BASE_DIR / "keys" / "private.pem",
        public_key_path=BASE_DIR / "keys" / "public.pem",
        algorithm="RS256",
        access_token_expire_minutes=15
    )


settings = Settings()
