from fastapi import APIRouter, HTTPException, Depends, Query
from ..models.profile import Profile
from ..models.user import User
from ..schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate, map_profile_to_response
from ..dependencies import get_current_user, authenticate
from ..core.orm import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.logger import logger
from ..core.exceptions import NotFoundException

# API Router
router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile: ProfileCreate,
    # auth: bool = Depends(authenticate),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info("start profile create")
    profile_data = profile.model_dump()
    logger.info(f"profile_data:{profile_data}")
    flat_data = {
        **profile_data["personal_info"],
        **profile_data["contact_info"],
        **profile_data["address"],
        "create_user": "current_user.username",
        "update_user": "current_user.username"
    }
    db_profile = Profile(**flat_data)
    logger.info(f"db_profile:{db_profile}")
    try:
        db.add(db_profile)
        await db.commit()
        await db.refresh(db_profile)
    except Exception as e:
        logger.error(str(e))
        raise Exception(e)

    logger.info(f"Profile created by {"current_user.username"}: {db_profile.id}")
    return map_profile_to_response(db_profile)

@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Profile).filter_by(id=profile_id, is_deleted=False))
    profile = result.scalar_one_or_none()
    if not profile:
        logger.warning(f"Profile {profile_id} not found")
        raise NotFoundException()
    return map_profile_to_response(profile)

@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: str,
    profile_update: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Profile).filter_by(id=profile_id, is_deleted=False))
    profile = result.scalar_one_or_none()
    if not profile:
        logger.warning(f"Profile {profile_id} not found for update")
        raise NotFoundException()
    update_data = profile_update.dict(exclude_unset=True)
    if "personal_info" in update_data:
        for key, value in update_data["personal_info"].items():
            setattr(profile, key, value)
    if "contact_info" in update_data:
        for key, value in update_data["contact_info"].items():
            setattr(profile, key, value)
    if "address" in update_data:
        for key, value in update_data["address"].items():
            setattr(profile, key, value)
    profile.update_user = current_user.username
    await db.commit()
    await db.refresh(profile)
    logger.info(f"Profile {profile_id} updated by {current_user.username}")
    return map_profile_to_response(profile)

@router.delete("/{profile_id}")
async def delete_profile(
    profile_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Profile).filter_by(id=profile_id, is_deleted=False))
    profile = result.scalar_one_or_none()
    if not profile:
        logger.warning(f"Profile {profile_id} not found for deletion")
        raise NotFoundException()
    profile.is_deleted = True
    profile.update_user = current_user.username
    await db.commit()
    logger.info(f"Profile {profile_id} soft-deleted by {current_user.username}")
    return {"message": "Profile soft-deleted"}

@router.get("/", response_model=list[ProfileResponse])
async def list_profiles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Profile).filter_by(is_deleted=False).offset(offset).limit(page_size)
    )
    profiles = result.scalars().all()
    logger.info(f"Profiles listed by {current_user.username}, page {page}, size {page_size}")
    return [map_profile_to_response(profile) for profile in profiles]