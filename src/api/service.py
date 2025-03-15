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
    db_service = Service(**service.dict(), create_user=current_user.username, update_user=current_user.username)
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
    for key, value in service_update.dict(exclude_unset=True).items():
        setattr(service, key, value)
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