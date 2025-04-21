from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .schemas import TransactionCreate, TransactionUpdate
from models import Transaction, User, Category
from .exceptions import Transaction404Error
from api.users.crud import update_user


async def get_transaction(session: AsyncSession, id: int):
    t = await session.scalar(
        select(Transaction)
        .where(Transaction.id == id)
    )
    if not t:
        raise Transaction404Error()
    return t


async def create_transaction(
    session: AsyncSession, data: TransactionCreate
) -> Transaction:
    u = session.get(User, data.user_id)
    c = session.get(Category, data.category_id)
    if (not u): raise ...
    transaction = Transaction(
        type=data.type,
        amount=data.amount,
        description=data.description,
        category_id=data.category_id,
        user_id=data.user_id,
    )
    session.add(transaction)
    await session.commit()
    return transaction


async def delete_transaction(session: AsyncSession, id: int) -> Transaction:
    t = await get_transaction(session, id)
    await session.delete(t)
    await session.commit()
    return t


async def update_transaction(
    session: AsyncSession,
    id: int,
    data: TransactionUpdate,
) -> Transaction:
    t = await get_transaction(session, id)
    if data.type:
        t.type = data.type
    if data.amount:
        t.amount = data.amount
    if data.user_id:
        t.user_id = data.user_id
    if data.category_id:
        t.category_id = data.category_id

    await session.commit()
    return t


async def get_transactions(session: AsyncSession) -> list[Transaction]:
    transactions = await session.scalars(
        select(Transaction)
        .order_by(Transaction.id)
        )
    transactions = [t for t in transactions]
    return transactions
