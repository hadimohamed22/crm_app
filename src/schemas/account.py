from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Address(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None

class PaymentInfo(BaseModel):
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    card_number: Optional[str] = None

class AccountBase(BaseModel):
    profile_id: UUID
    address: Address
    payment_info: PaymentInfo
    account_status: Optional[str] = "active"

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    address: Optional[Address] = None
    payment_info: Optional[PaymentInfo] = None
    account_status: Optional[str] = None

class AccountResponse(AccountBase):
    id: UUID
    create_date: str
    update_date: str
    create_user: str
    update_user: str
    is_deleted: bool

    class Config:
        from_attributes = True