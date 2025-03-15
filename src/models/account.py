from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from ..core.models import BaseModel

class Account(BaseModel):
    __tablename__ = "accounts"

    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False)
    
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)

    bank_account_number = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    card_number = Column(String, nullable=True)
    account_status = Column(String, default="active")      # e.g., "active", "inactive", "pending"