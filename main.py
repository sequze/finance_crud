from fastapi import FastAPI
from contextlib import asynccontextmanager
from db_helper import db_helper

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with db_helper.engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.create_all)
#     yield

app = FastAPI()