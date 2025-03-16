from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .core.config import config
from .models.user import User
from .core.orm import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime, timedelta, timezone
from .core.logger import logger
from .core.exceptions import UnauthorizedException


SECRET_KEY = config.get("auth", {}).get("secret_key", "your-secret-key")
ALGORITHM = config.get("auth", {}).get("algorithm", "HS256")
REQ_AUTH = config.get("app", {}).get("require_auth", False)
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("auth", {}).get("access_token_expire_minutes", 30)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    # Check if authentication is disabled via config
    logger.debug("********get_current_user")
    logger.info(f"Auth status: {REQ_AUTH}")
    if not REQ_AUTH: 
        # Return a default "anonymous" user when auth is disabled
        logger.debug("Auth disabled")
        result = await db.execute(select(User).filter_by(username="anonymous"))
        user = result.scalar_one_or_none()
        if not user:
            # Create anonymous user if it doesn't exist
            user = User(username="anonymous", email="anonymous@example.com", hashed_password="")
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    # Normal authentication logic when enabled
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).filter_by(username=username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user