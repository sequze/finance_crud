from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import TransactionSchema, TransactionCreate, TransactionUpdate
from models import db_helper
from . import crud

router = APIRouter(tags=["Transactions"])

@router.get("/", response_model=list[TransactionSchema])
async def get_transactions(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await crud.get_transactions(session)


@router.post("/create_transaction", response_model=TransactionSchema)
async def create_transaction(
    transaction: TransactionCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    t = await crud.create_transaction(session, transaction)
    return t


@router.post("/{transaction_id}", response_model=TransactionSchema)
async def get_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        t = await crud.get_transaction(session, transaction_id)
    except ValueError:
        raise HTTPException(404, "Transaction not found!")
    return t


@router.patch("/{transaction_id}", response_model=TransactionSchema)
async def update_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)    
):
    try: 
        t = await crud.update_transaction(session, transaction_id, transaction)
    except ValueError:
        raise HTTPException(404, "Transaction not found!")
    return t


@router.delete("/{transaction_id}", response_model=TransactionSchema)
async def delete_transaction(
    transaction_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    try:
        t = await crud.delete_transaction(session, transaction_id)
    except ValueError:
        raise HTTPException(404, "Not found!")
    return t
