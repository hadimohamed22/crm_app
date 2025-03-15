from sqlalchemy import Column, String, ForeignKey, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from ..core.models import BaseModel

class Service(BaseModel):
    __tablename__ = "services"

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False)
    service_type = Column(String, nullable=False)  

    # Installation address
    installation_province = Column(String, nullable=True)
    installation_city = Column(String, nullable=True)
    installation_address = Column(String, nullable=True)
    installation_postal_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=True) 
    longitude = Column(Float, nullable=True) 

    # Service-specific fields
    msisdn = Column(String, nullable=True)  
    kit_number = Column(String, nullable=True) 
    imei = Column(String, nullable=True) 
    mac_id = Column(String, nullable=True) 
    status = Column(String, default="active") 
    shahkar_ref_id = Column(String, nullable=True) 

    # Date fields
    installation_date = Column(DateTime, nullable=True)
    confirmation_date = Column(DateTime, nullable=True)
    purchase_date = Column(DateTime, nullable=True)
    delivery_date = Column(DateTime, nullable=True)
    activation_date = Column(DateTime, nullable=True)
    cancelation_date = Column(DateTime, nullable=True)
    registration_date = Column(DateTime, nullable=True)