from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class InstallationAddress(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ServiceIdentifiers(BaseModel):
    msisdn: Optional[str] = None
    lit_number: Optional[str] = None
    imei: Optional[str] = None
    mac_id: Optional[str] = None

class ServiceDates(BaseModel):
    installation_date: Optional[datetime] = None
    confirmation_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    activation_date: Optional[datetime] = None
    cancelation_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    
class ServiceBase(BaseModel):
    account_id: UUID
    service_type: str
    installation_address: InstallationAddress
    service_identifiers: ServiceIdentifiers
    status: Optional[str] = "pending"
    shahkar_ref_id: Optional[str] = None
    dates: ServiceDates

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_type: Optional[str] = None
    installation_address: Optional[InstallationAddress] = None
    service_identifiers: Optional[ServiceIdentifiers] = None
    status: Optional[str] = None
    shahkar_ref_id: Optional[str] = None
    dates: ServiceDates

class ServiceResponse(ServiceBase):
    id: UUID
    create_date: str
    update_date: str
    create_user: str
    update_user: str
    is_deleted: bool

    class Config:
        orm_mode = True