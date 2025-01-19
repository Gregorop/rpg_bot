import os
from functools import wraps
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
TESTING = os.getenv('TESTING')

if TESTING:
    PORT = os.getenv('DB_PORT_test')
else:
    PORT = os.getenv('DB_PORT')

engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{PORT}/{POSTGRES_DB}",
    poolclass=NullPool) #без этого путаются eventpolls от pytest и алхимии, лол

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
