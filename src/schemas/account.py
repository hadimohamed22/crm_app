from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class AccountBase(BaseModel):
    profile_id: UUID
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    card_number: Optional[str] = None
    account_status: Optional[str] = "active"

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    card_number: Optional[str] = None
    account_status: Optional[str] = None

class AccountResponse(AccountBase):
    id: UUID
    create_date: str
    update_date: str
    create_user: str
    update_user: str
    is_deleted: bool

    class Config:
        orm_mode = True