from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey
from typing import Optional
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class Category(Base):
    __tablename__ = "categories"
    name: Mapped[str]
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category",
                                                             cascade="all, delete")

