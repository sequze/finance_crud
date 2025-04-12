from models import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .schemas import CategoryUpdate


async def create_category(session: AsyncSession, name: str) -> Category:
    c = Category(name=name)
    session.add(c)
    await session.commit()
    return c


async def get_categories(session: AsyncSession) -> list[Category]:
    categories = await session.scalars(select(Category).order_by(Category.name))
    categories = [i for i in categories]
    return categories


async def get_category_by_id(session: AsyncSession,
                             id: int) -> Category | None:
    return await session.get(Category, id)


async def update_category(session: AsyncSession, category: CategoryUpdate, id: int) -> Category:
    c = await session.get(Category, id)
    if (not c): raise ValueError("Not found")
    c.name = category.name
    await session.commit()
    return c


async def delete_category(session: AsyncSession, id: int) -> Category:
    c = await session.get(Category, id)
    if (not c): raise ValueError("Not found")
    await session.delete(c)
    await session.commit()
    return c
