from models import User, db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from asyncio import run
from .schemas import UserCreate
async def get_users(session: AsyncSession) -> list[User]:
    res = await session.scalars(select(User).order_by(User.id))
    users = [user for user in res]
    return users
    
async def get_user_by_id(session:AsyncSession, id: int) -> User:
    ...
    
async def create_user(session: AsyncSession, user_create: UserCreate):
    check: User | None = await session.scalar(select(User).where(User.username == user_create.username))
    if not check:
        u = User(username=user_create.username, balance=user_create.balance)
        session.add(u)
        await session.commit()
        return u
    raise ValueError(f"User with username {user_create.username} already exists")

async def update_user():
    ...
    
async def delete_user():
    ...
    

async def main():
    async with db_helper.session_factory() as session:
        res = await get_users(session=session)
        print(res)