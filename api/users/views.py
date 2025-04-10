from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import User, UserCreate, UserUpdate
router = APIRouter(tags=["Users"])
from models.db_helper import db_helper
from sqlalchemy import select
from . import crud
from models import User as DbUser

#TODO: структурировать нормально
@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ):
    return await crud.get_users(session)


@router.post("/", response_model=User)
async def get_user_by_id(
    id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    u = await crud.get_user_by_id(session, id)
    if u is None:
        raise HTTPException(404, "User not found!")
    else: return u


@router.post("/create_user", response_model=User)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    u = await crud.create_user(session, user)
    return u


@router.patch("/edit_user", response_model=User)
async def update_user(
    id: int,
    user_update: UserUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    u = await session.get(DbUser, id)
    if not u: raise HTTPException(404, "User not found!")
    return await crud.update_user(session, u, user_update)


@router.delete("/delete_user")
async def delete_user(
    id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    u = await session.get(DbUser, id)
    if u is None: raise HTTPException(404, "User is not found!")
    await crud.delete_user(session, u)
