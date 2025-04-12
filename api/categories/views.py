from fastapi import APIRouter, Depends, HTTPException
from models.db_helper import db_helper
from .schemas import CategorySchema, CategoryUpdate, CategoryCreate
from . import crud
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter(tags=["Categories"])

@router.post("/create_category", response_model=CategorySchema)
async def create_category(
    cat: CategoryCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    cat = await crud.create_category(session, cat.name)
    return cat

@router.get("/", response_model=list[CategorySchema])
async def get_categories(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    categories = await crud.get_categories(session)
    return categories


@router.post("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        cat = await crud.get_category_by_id(session, category_id)
        return cat
    except ValueError:
        raise HTTPException(404, "Category not found")


@router.patch("/{category_id}", response_model=CategorySchema)    
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        cat = await get_category_by_id(session=session,
                                 category_id=category_id)
    except ValueError: raise HTTPException(404, "Not Found")
    if (category.name): cat.name = category.name
    session.commit()
    return cat


@router.delete("/{category_id}", response_model=CategorySchema)
async def delete_category(
    id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    try:
        cat = await crud.delete_category(session, id)
    except ValueError:
        raise HTTPException("Not Found")
    return cat
