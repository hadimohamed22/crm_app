from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str