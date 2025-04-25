from .base import Base
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .transaction import Transaction
class User(Base):
    username: Mapped[str]
    balance: Mapped[int]
    password_hash: Mapped[str]
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user",
                                                             cascade="all, delete")
