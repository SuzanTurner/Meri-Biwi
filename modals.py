from database import Base
from sqlalchemy import Column, Integer,Float, String, DateTime, Enum,Text,Boolean
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(String(15), nullable=False)
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
    status = Column(nullable = False, default = "Pending")
    
   


class CategoryEnum(str, enum.Enum):
    cleaning = "cleaning"
    cooking = "cooking"
    baby_care = "Baby Care"
    elder_care = "Elder Care"


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    features = Column(ARRAY(String),nullable=False)  # Can store comma-separated features or JSON string
    description = Column(Text)
    price = Column(Float, nullable=False)
    duration = Column(String)  # e.g., "2 hours", "30 mins"
    is_popular = Column(Boolean, default=False)