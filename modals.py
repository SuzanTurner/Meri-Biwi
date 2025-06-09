from database import Base
from sqlalchemy import Column, Integer,Float, String, DateTime, Enum,Text,Boolean
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
import pytz
import enum

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(String(15),unique=True, nullable=False)
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
    
    religion = Column(nullable = False, default = "God knows")
    


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
    
    
# class User_Login(Base):
#     __tablename__ = "logins"
    
#     id = Column(Integer, primary_key = True, index = True)
#     username = Column(String, nullable = False)
#     password = Column(String, nullable = False)

ist = pytz.timezone("Asia/Kolkata")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index = True)
    uid = Column(String, unique = True, nullable = False)
    phone = Column(String(15), unique=True, nullable=False)
    email = Column(String, unique = True, nullable=False)
    password = Column(String, nullable = False)
    avatar = Column(String(15), default = "avatar", nullable=False)
    otp_verified = Column(Boolean, nullable = False)
    fcm_token = Column(String, default = "fcm_token", nullable=False)
    wallet = Column(Float, default = 0.00, nullable=False)
    status = Column(Boolean, default = False, nullable=False)
    address_line_1 = Column(String, nullable=False)
    address_line_2 = Column(String, nullable=False)
    city = Column(String, nullable=False)
    longitude = Column(String, default = " latitude" ,nullable=False)
    latitude = Column(String, default = "longitude" ,nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(ist))
    updated_at = Column(DateTime, default=lambda: datetime.now(ist))
    
class UserLogin(Base):
    __tablename__ = "user_logins"
    
    id = Column(Integer, primary_key=True, autoincrement= True, index = True, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(DateTime, default=lambda : datetime.now(ist))
    