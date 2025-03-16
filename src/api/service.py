from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.orm import get_db
from ..core.logger import logger
from ..core.exceptions import NotFoundException
from ..dependencies import get_current_user
from ..models.user import User
from ..models.service import Service
from ..schemas.service import ServiceCreate, ServiceUpdate, ServiceResponse
from sqlalchemy.future import select

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceResponse)
async def create_service(
    service: ServiceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service_data = service.model_dump()
    flat_data = {
        "account_id": service_data["account_id"],
        "service_type": service_data["service_type"],
        **service_data["installation_address"],
        **service_data["service_identifiers"],
        "status": service_data["status"],
        "shahkar_ref_id": service_data["shahkar_ref_id"],
        "installation_date": service_data["installation_date"],
        "confirmation_date": service_data["confirmation_date"],
        "purchase_date": service_data["purchase_date"],
        "delivery_date": service_data["delivery_date"],
        "activation_date": service_data["activation_date"],
        "cancelation_date": service_data["cancelation_date"],
        "registration_date": service_data["registration_date"]
    }
    db_service = Service(**flat_data, create_user=current_user.username, update_user=current_user.username)
    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    logger.info(f"Service created by {current_user.username}: {db_service.id}")
    return db_service

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Service).filter_by(id=service_id, is_deleted=False))
    service = result.scalar_one_or_none()
    if not service:
        logger.warning(f"Service {service_id} not found")
        raise NotFoundException()
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: str,
    service_update: ServiceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Service).filter_by(id=service_id, is_deleted=False))
    service = result.scalar_one_or_none()
    if not service:
        logger.warning(f"Service {service_id} not found for update")
        raise NotFoundException()
    update_data = service_update.dict(exclude_unset=True)
    if "installation_address" in update_data:
        for key, value in update_data["installation_address"].items():
            setattr(service, key, value)
    if "service_identifiers" in update_data:
        for key, value in update_data["service_identifiers"].items():
            setattr(service, key, value)
    for key in ["service_type", "status", "shahkar_ref_id", "installation_date", "confirmation_date", 
                "purchase_date", "delivery_date", "activation_date", "cancelation_date", "registration_date"]:
        if key in update_data:
            setattr(service, key, update_data[key])
    service.update_user = current_user.username
    await db.commit()
    await db.refresh(service)
    logger.info(f"Service {service_id} updated by {current_user.username}")
    return service

@router.delete("/{service_id}")
async def delete_service(
    service_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Service).filter_by(id=service_id, is_deleted=False))
    service = result.scalar_one_or_none()
    if not service:
        logger.warning(f"Service {service_id} not found for deletion")
        raise NotFoundException()
    service.is_deleted = True
    service.update_user = current_user.username
    await db.commit()
    logger.info(f"Service {service_id} soft-deleted by {current_user.username}")
    return {"message": "Service soft-deleted"}

@router.get("/", response_model=list[ServiceResponse])
async def list_services(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Service).filter_by(is_deleted=False).offset(offset).limit(page_size)
    )
    services = result.scalars().all()
    logger.info(f"Services listed by {current_user.username}, page {page}, size {page_size}")
    return services