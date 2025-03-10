from sqlalchemy import create_engine
from ..core.orm import Base
from ..models.user import User
from ..models.profile import Profile
from ..core.config import config

def init_db():
    # Use synchronous engine for table creation
    db_url = config.get("database", {}).get("url", "sqlite+aiosqlite:///crm.db").replace("sqlite+aiosqlite:///", "sqlite:///")
    engine = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")

if __name__ == "__main__":
    init_db()