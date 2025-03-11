from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional

class ProfileCreate(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str] = None
    national_id: Optional[str] = None
    birth_cert_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    identification_type: Optional[str] = None
    tel_number: Optional[str] = None
    tel_code: Optional[str] = None
    mobile_number: Optional[str] = None
    emergency_phone_number: Optional[str] = None
    preferred_language: Optional[str] = None
    email: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    unit: Optional[str] = None
    floor: Optional[int] = None
    plaque: Optional[str] = None

class ProfileResponse(ProfileCreate):
    id: UUID
    create_date: datetime
    update_date: datetime
    is_deleted: bool
    create_user: str
    update_user: str

    class Config:
        from_attributes = True