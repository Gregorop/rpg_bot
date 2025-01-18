import pytest_asyncio
from db import engine, async_session_maker

from models import Base

@pytest_asyncio.fixture
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest_asyncio.fixture
async def session():
    async with async_session_maker() as session:
        yield session