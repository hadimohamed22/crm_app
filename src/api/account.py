from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.orm import get_db
from ..core.logger import logger
from ..core.exceptions import NotFoundException
from ..dependencies import get_current_user
from ..models.user import User
from ..models.account import Account
from ..schemas.account import AccountCreate, AccountUpdate, AccountResponse
from sqlalchemy.future import select

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountResponse)
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_account = Account(**account.model_dump(), create_user=current_user.username, update_user=current_user.username)
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    logger.info(f"Account created by {current_user.username}: {db_account.id}")
    return db_account

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Account).filter_by(id=account_id, is_deleted=False))
    account = result.scalar_one_or_none()
    if not account:
        logger.warning(f"Account {account_id} not found")
        raise NotFoundException()
    return account

@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: str,
    account_update: AccountUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Account).filter_by(id=account_id, is_deleted=False))
    account = result.scalar_one_or_none()
    if not account:
        logger.warning(f"Account {account_id} not found for update")
        raise NotFoundException()
    for key, value in account_update.dict(exclude_unset=True).items():
        setattr(account, key, value)
    account.update_user = current_user.username
    await db.commit()
    await db.refresh(account)
    logger.info(f"Account {account_id} updated by {current_user.username}")
    return account

@router.delete("/{account_id}")
async def delete_account(
    account_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Account).filter_by(id=account_id, is_deleted=False))
    account = result.scalar_one_or_none()
    if not account:
        logger.warning(f"Account {account_id} not found for deletion")
        raise NotFoundException()
    account.is_deleted = True
    account.update_user = current_user.username
    await db.commit()
    logger.info(f"Account {account_id} soft-deleted by {current_user.username}")
    return {"message": "Account soft-deleted"}

@router.get("/", response_model=list[AccountResponse])
async def list_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Account).filter_by(is_deleted=False).offset(offset).limit(page_size)
    )
    accounts = result.scalars().all()
    logger.info(f"Accounts listed by {current_user.username}, page {page}, size {page_size}")
    return accounts