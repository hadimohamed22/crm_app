from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BaseResponseModel(BaseModel):
    id: UUID
    create_date: str = datetime.now()
    update_date: str = datetime.now()
    create_user: str = "anonymous@example.com"
    update_user: str = "anonymous@example.com"
    is_deleted: bool = False
