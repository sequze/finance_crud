from pydantic import BaseModel, PositiveInt, ConfigDict
from typing import Literal
from api.categories.schemas import CategorySchema
from api.users.schemas import User

class TransactionBase(BaseModel):
    type: Literal["income", "expense"]
    amount: PositiveInt
    description: str | None = None
    user_id: int
    category_id: int


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    type: Literal['income', 'expense'] | None = None
    amount: PositiveInt | None = None
    user_id: int | None = None
    category_id: int | None = None


class TransactionSchema(TransactionBase):
    type: str
    model_config = ConfigDict(from_attributes=True)