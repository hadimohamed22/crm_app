from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import config

DATABASE_URL = config.get("database", {}).get("url", "sqlite+aiosqlite:///crm.db")
engine = create_async_engine(DATABASE_URL, echo=config.get("database", {}).get("echo", False))
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session