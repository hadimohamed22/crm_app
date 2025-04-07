from pydantic import BaseModel
from datetime import date, datetime
from uuid import UUID
from typing import Optional
from ..models.profile import Profile

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
        
def map_profile_to_response(profile: Profile) -> ProfileResponse:
    return ProfileResponse(
        id=profile.id,
        personal_info=PersonalInfo(
            first_name= profile.first_name,
            last_name= profile.last_name,
            father_name= profile.father_name,
            national_id= profile.national_id,
            birth_cert_number= profile.birth_cert_number,
            date_of_birth= profile.date_of_birth,
            gender= profile.gender,
            nationality= profile.nationality,
            identification_type= profile.identification_type,
            preferred_language= profile.preferred_language
        ),
        contact_info=ContactInfo(
            tel_number= profile.tel_number,
            tel_code= profile.tel_code,
            mobile_number= profile.mobile_number,
            emergency_phone_number= profile.emergency_phone_number,
            email= profile.email
        ),
        address=Address(
            province= profile.province,
            city= profile.city,
            address= profile.address,
            postal_code= profile.postal_code,
            latitude= profile.latitude,
            longitude= profile.longitude,
            unit= profile.unit,
            floor= profile.floor,
            plaque= profile.plaque
        ),
        create_date=profile.create_date,
        update_date=profile.update_date,
        is_deleted=profile.is_deleted,
        create_user=profile.create_user,
        update_user=profile.update_user
    )