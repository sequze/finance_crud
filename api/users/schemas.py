from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    balance: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None = None
    balance: int | None = None


class User(UserBase):
    model_config=ConfigDict(from_attributes=True)
    id: int