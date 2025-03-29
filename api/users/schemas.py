from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    balance: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int