from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from ..models.account import Account
from .base import BaseResponseModel


class Address(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None


class PaymentInfo(BaseModel):
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    card_number: Optional[str] = None


class ProfileDetails(BaseModel):
    id: UUID


class AccountBase(BaseModel):
    profile: ProfileDetails
    address: Address
    payment_info: PaymentInfo
    account_status: Optional[str] = "active"


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    address: Optional[Address] = None
    payment_info: Optional[PaymentInfo] = None
    account_status: Optional[str] = None


class AccountResponse(AccountBase, BaseResponseModel):
    class Config:
        from_attributes = True


def map_account_to_response(account: Account) -> AccountResponse:
    return AccountResponse(
        id=account.id,
        profile=ProfileDetails(
            id=account.profile_id,
        ),
        address=Address(
            province=account.province,
            city=account.city,
            address=account.address,
            postal_code=account.postal_code,
        ),
        payment_info=PaymentInfo(
            bank_account_number=account.bank_account_number,
            bank_name=account.bank_name,
            card_number=account.card_number,
        ),
        account_status=account.account_status,
        create_date=account.create_date,
        update_date=account.update_date,
        create_user=account.create_user,
        update_user=account.update_user,
        is_deleted=account.is_deleted,
    )
