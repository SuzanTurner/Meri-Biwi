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
    
class User_Login(Base):
    __tablename__ = "logins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

# SERVICES
class CategoryEnum(str, enum.Enum):
    cleaning = "cleaning"
    cooking = "cooking"
    baby_care = "baby_care"
    elder_care = "elder_care"
class FoodTypeEnum(str, enum.Enum):
    veg = "Veg"
    non_veg = "Non-veg"


class PlanTypeEnum(str, enum.Enum):
    basic = "basic"
    standard = "standard"
    premium = "premium"

# Making this for Cooking and Cleaning Only. 
class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    plan_type = Column(Enum(PlanTypeEnum), nullable=False)
    frequency = Column(Integer, nullable=False)
    number_of = Column(Integer, nullable=False)
    basic_price=Column(Float,nullable=False)
    basic_details = Column(ARRAY(String), nullable=False)
    description = Column(Text)

    
    # Can store comma-separated features or JSON string
    
    duration = Column(Float, nullable=False)  # months or days?
    
    food_type = Column(Enum(FoodTypeEnum), nullable=True)
    is_popular = Column(Boolean, default=False)
    

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
    
    otp = Column(String, nullable=True) 
    otp_created_at = Column(DateTime, default=lambda : datetime.utcnow())
    
class UserLogin(Base):
    __tablename__ = "user_logins"
    
    id = Column(Integer, primary_key=True, autoincrement= True, index = True, nullable = False)
    email = Column(String, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(DateTime, default=lambda : datetime.now(ist))
    
class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(Integer, primary_key=True, autoincrement= True, index = True, nullable = False)
    username = Column(String, nullable=False)
    email = Column(String, unique = True, nullable=False)
    password = Column(String, unique = True, nullable=False)
    full_name = Column(String, nullable=False)
    profile_image = Column(String)
    role = Column(String, default = "Admin", nullable=False)
    status = Column(Boolean, default = False, nullable=False)
    created_at = Column(DateTime, default=lambda : datetime.now(ist))
    

    basic_price = Column(Float, nullable=False)
    

class AdditionalFeature(Base):
    __tablename__ = "service_additional_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)