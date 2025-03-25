from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

class Transaction(Base):
    type: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    description: Optional[str]
    # добавить время
