from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):

    @declared_attr.directive # показывает, что мы генерируем аттрибут класса - наследника
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
