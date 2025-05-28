from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(Integer, nullable=False)
    address = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False, index=True)
    gender = Column(String, nullable=False, index=True)
    dob = Column(String, nullable=False)

    service = Column(String, nullable=False, index=True)
    exp = Column(Integer, nullable=False)
    availability = Column(String, nullable=False, index=True)
    id_proof = Column(String, nullable=False, index=True)
    id_proof_number = Column(String, nullable=False, index=True)
    about = Column(String, nullable=False)

    photo_path = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
