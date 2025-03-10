from sqlalchemy import Column, String, Integer, Date, Float
from ..core.models import BaseModel

class Profile(BaseModel):
    __tablename__ = "profiles"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    father_name = Column(String, nullable=True)
    national_id = Column(String, unique=True, index=True, nullable=True)
    birth_cert_number = Column(String, unique=True, index=True, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    nationality = Column(String, nullable=True)
    identification_type = Column(String, nullable=True)
    tel_number = Column(String, nullable=True)
    tel_code = Column(String, nullable=True)
    mobile_number = Column(String, unique=True, index=True, nullable=True)
    emergency_phone_number = Column(String, nullable=True)
    preferred_language = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    province = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    unit = Column(String, nullable=True)
    floor = Column(Integer, nullable=True)
    plaque = Column(String, nullable=True)

    def __repr__(self):
        return f"<Profile(id={self.id}, first_name={self.first_name}, last_name={self.last_name})>"