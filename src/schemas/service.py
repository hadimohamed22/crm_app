from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from ..models.service import Service

class InstallationAddress(BaseModel):
    province: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ServiceIdentifiers(BaseModel):
    msisdn: Optional[str] = None
    kit_number: Optional[str] = None
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
   
class  AccountDetails(BaseModel):
    id: UUID
    
class ServiceBase(BaseModel):
    account: AccountDetails
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
        from_attributes = True
        
def map_service_to_response(service: Service) -> ServiceResponse:
    return ServiceResponse(
        id=service.id,
        account=AccountDetails(
            id=service.account_id
        ),
        service_type=service.service_type,
        installation_address= InstallationAddress(
            province=service.installation_province,
            city=service.installation_city,
            address=service.installation_address,
            postal_code=service.installation_postal_code,
            latitude=service.latitude,
            longitude=service.longitude,
        ),
        service_identifiers=ServiceIdentifiers(
            msisdn= service.msisdn,
            kit_number= service.kit_number,
            imei= service.imei,
            mac_id= service.mac_id,
        ),
        status= service.status,
        shahkar_ref_id= service.shahkar_ref_id,
        dates=ServiceDates(
            installation_date= service.installation_date,
            confirmation_date= service.confirmation_date,
            purchase_date= service.purchase_date,
            delivery_date= service.delivery_date,
            activation_date= service.activation_date,
            cancelation_date= service.cancelation_date,
            registration_date= service.registration_date,
        ),
        create_date=service.create_date,
        update_date=service.update_date,
        is_deleted=service.is_deleted,
        create_user=service.create_user,
        update_user=service.update_user
        )