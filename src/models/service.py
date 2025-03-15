from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from ..core.models import BaseModel

class Service(BaseModel):
    __tablename__ = "services"

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    service_type = Column(String, nullable=False)  # e.g., "internet", "mobile", "tv"

    # Installation address
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    lat = Column(Float, nullable=True)  # Latitude
    long = Column(Float, nullable=True)  # Longitude

    # Service-specific fields
    msisdn = Column(String, nullable=True)         # Mobile Subscriber ISDN (phone number)
    lit_number = Column(String, nullable=True)     # Line identification number
    imei = Column(String, nullable=True)           # Device IMEI
    mac_id = Column(String, nullable=True)         # MAC address
    status = Column(String, default="pending")     # e.g., "pending", "active", "canceled"
    shahkar_ref_id = Column(String, nullable=True) # Reference ID (e.g., for Shahkar system in Iran)

    # Date fields
    installation_date = Column(DateTime, nullable=True)
    confirmation_date = Column(DateTime, nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    delivery_date = Column(DateTime, nullable=True)
    activation_date = Column(DateTime, nullable=True)
    cancelation_date = Column(DateTime, nullable=True)
    registration_date = Column(DateTime, nullable=True)