from pydantic import BaseModel, PositiveInt
from typing import Literal


class TransactionBase(BaseModel):
    type: Literal["income", "expense"]
    amount: PositiveInt
    description: str | None = None
    
class TransactionCreate(TransactionBase):
    user_id: int
    category_id: int


class TransactionUpdate(TransactionBase):
    type: Literal['income', 'expense'] | None = None
    amount: PositiveInt | None = None
    user_id: int | None = None
    category_id: int | None = None
