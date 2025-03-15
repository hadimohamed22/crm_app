from sqlalchemy import create_engine
from ..core.orm import Base
from ..models.user import User
from ..models.profile import Profile
from ..models.account import Account
from ..models.service import Service
from ..core.config import config

def init_db():
    db_url = config.get("database", {}).get("url", "").replace("postgresql+asyncpg://", "postgresql://")
    engine = create_engine(db_url, echo=config.get("database", {}).get("echo", False))
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()