from .base import Base
from sqlalchemy.orm import Mapped

class User(Base):
    name: Mapped[str]
    balance: Mapped[int]
    