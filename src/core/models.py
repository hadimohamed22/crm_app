from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .orm import Base

class AuditModel:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    update_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    create_user = Column(String, default="system")
    update_user = Column(String, default="system")

class SoftDeleteModel:
    is_deleted = Column(Boolean, default=False, nullable=False)

class BaseModel(AuditModel, SoftDeleteModel, Base):
    __abstract__ = True