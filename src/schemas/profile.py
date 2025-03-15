from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional

class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    father_name: Optional[str] = None
    national_id: Optional[str] = None
    birth_cert_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    identification_type: Optional[str] = None
    preferred_language: Optional[str] = None
    
class ContactInfo(BaseModel):
    tel_number: Optional[str] = None
    tel_code: Optional[str] = None
    mobile_number: Optional[str] = None
    emergency_phone_number: Optional[str] = None
    email: Optional[str] = None
  
class Address(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    unit: Optional[str] = None
    floor: Optional[int] = None
    plaque: Optional[str] = None
          
class ProfileCreate(BaseModel):
    personal_info: PersonalInfo
    contact_info: ContactInfo
    address: Address

class ProfileUpdate(BaseModel):
    personal_info: Optional[PersonalInfo] = None
    contact_info: Optional[ContactInfo] = None
    address: Optional[Address] = None
    
class ProfileResponse(ProfileCreate):
    id: UUID
    create_date: datetime
    update_date: datetime
    is_deleted: bool
    create_user: str
    update_user: str

    class Config:
        from_attributes = True