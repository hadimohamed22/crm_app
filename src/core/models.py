from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from .orm import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    create_date = Column(DateTime, default=datetime.now())
    update_date = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    create_user = Column(String, default="system")
    update_user = Column(String, default="system")
    is_deleted = Column(Boolean, default=False)