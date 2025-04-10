from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    async_scoped_session, AsyncSession
from config import settings
from asyncio import current_task



class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Создаем движок бд и фабрику сессий
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(bind=self.engine,
                                                  autoflush=False,
                                                  autocommit=False,
                                                  expire_on_commit=False)

    def create_scoped_session(self) -> AsyncSession:
        scoped_session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task
        )
        return scoped_session
    
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.create_scoped_session()
        yield session
        await session.close()
            

db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)