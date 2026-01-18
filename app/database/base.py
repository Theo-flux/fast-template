from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import Config

async_engine: AsyncEngine = create_async_engine(url=Config.DATABASE_URL)
AsyncSessionMaker = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initializes the connection with the database."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Creates an asynchronous session for the database"""
    async with AsyncSessionMaker() as async_session_maker:
        yield async_session_maker
