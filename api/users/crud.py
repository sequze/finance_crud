from models import User, db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .schemas import UserCreate, UserUpdate
from .exceptions import UserNotFoundException
from api.auth.jwt_tools import hash_pwd
#TODO: переделать функции чтобы работали с бд, а не принимали экземпляры User
async def get_users(session: AsyncSession) -> list[User]:
    res = await session.scalars(select(User).order_by(User.id))
    users = [user for user in res]
    return users


async def get_user_by_id(session: AsyncSession, id: int) -> User:
    u = await session.get(User, id)
    if not u:
        raise UserNotFoundException()
    return u


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    u = await session.scalar(
        select(User)
        .where(
            User.username == username)
    )
    if not u:
        raise UserNotFoundException()
    return u


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    check = await session.scalar(select(User)
                                 .where(User.username==user_create.username))
    if not check:
        u = User(
            username=user_create.username, 
            balance=user_create.balance, 
            password_hash=hash_pwd(user_create.password)
            )
        session.add(u)
        await session.commit()
        return u
    raise ValueError(f"User with username {user_create.username} already exists")


async def update_user(session: AsyncSession, user: User, user_update: UserUpdate) -> User:
    if user_update.username:
        user.username = user_update.username
    if user_update.balance is not None:
        user.balance = user_update.balance
    await session.commit()
    return user


async def delete_user(session: AsyncSession, user: User):
    await session.delete(user)
    await session.commit()
