from fastapi import APIRouter, HTTPException, Depends
from ..models.profile import Profile
from ..models.user import User
from ..schemas.profile import ProfileCreate, ProfileResponse
from ..dependencies import get_current_user
from ..core.orm import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=ProfileResponse)
async def create_profile(profile: ProfileCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    db_profile = Profile(**profile.dict(), create_user=current_user.username)
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile

@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(profile_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).filter_by(id=profile_id, is_deleted=False))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found or deleted")
    return profile

@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(profile_id: str, profile_update: ProfileCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).filter_by(id=profile_id, is_deleted=False))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found or deleted")
    for key, value in profile_update.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    profile.update_user = current_user.username
    await db.commit()
    await db.refresh(profile)
    return profile

@router.delete("/{profile_id}")
async def delete_profile(profile_id: str, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).filter_by(id=profile_id, is_deleted=False))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found or deleted")
    profile.is_deleted = True
    profile.update_user = current_user.username
    await db.commit()
    return {"message": "Profile soft-deleted"}

@router.get("/", response_model=list[ProfileResponse])
async def list_profiles(page: int = 1, page_size: int = 10, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * page_size
    result = await db.execute(select(Profile).filter_by(is_deleted=False).offset(offset).limit(page_size))
    return result.scalars().all()