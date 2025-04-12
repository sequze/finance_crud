from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from typing import Optional
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import User
    from .categories import Category


class Transaction(Base):
    type: Mapped[str] # доход / расход
    amount: Mapped[int]
    description: Mapped[str] = mapped_column(nullable=True)
    time: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    # relationships
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    category: Mapped["Category"] = relationship(back_populates="transactions")
    user: Mapped["User"] = relationship(back_populates="transactions")

