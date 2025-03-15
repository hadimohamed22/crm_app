from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import config

DATABASE_URL = config.get("database", "url", "sqlite+aiosqlite:///crm.db")
ECHO = config.get("database", "echo", False)
engine = create_async_engine(DATABASE_URL, echo=ECHO)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session