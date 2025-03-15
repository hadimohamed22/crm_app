from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ServiceBase(BaseModel):
    account_id: UUID
    service_type: str
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    msisdn: Optional[str] = None
    lit_number: Optional[str] = None
    imei: Optional[str] = None
    mac_id: Optional[str] = None
    status: Optional[str] = "pending"
    shahkar_ref_id: Optional[str] = None
    installation_date: Optional[datetime] = None
    confirmation_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    activation_date: Optional[datetime] = None
    cancelation_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_type: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    msisdn: Optional[str] = None
    lit_number: Optional[str] = None
    imei: Optional[str] = None
    mac_id: Optional[str] = None
    status: Optional[str] = None
    shahkar_ref_id: Optional[str] = None
    installation_date: Optional[datetime] = None
    confirmation_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    activation_date: Optional[datetime] = None
    cancelation_date: Optional[datetime] = None
    registration_date: Optional[datetime] = None

class ServiceResponse(ServiceBase):
    id: UUID
    create_date: str
    update_date: str
    create_user: str
    update_user: str
    is_deleted: bool

    class Config:
        orm_mode = True