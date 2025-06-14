from database import Base
from sqlalchemy import Column, Integer,Float, String, DateTime, Enum,Text,Boolean, ForeignKey
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
import pytz

import enum

# class Worker(Base):
#     __tablename__ = "workers"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False, index=True)
#     email = Column(String, nullable=False, index=True)
#     phone = Column(String(15),unique=True, nullable=False)
#     address = Column(String, nullable=False, index=True)
#     city = Column(String, nullable=False, index=True)
#     gender = Column(String, nullable=False, index=True)
#     dob = Column(String, nullable=False)

#     service = Column(String, nullable=False, index=True)
#     exp = Column(Integer, nullable=False)
#     availability = Column(String, nullable=False, index=True)
#     id_proof = Column(String, nullable=False, index=True)
#     id_proof_number = Column(String, nullable=False, index=True)
#     about = Column(String, nullable=False)

#     photo_path = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     status = Column(nullable = False, default = "Pending")
    
#     religion = Column(nullable = False, default = "God knows")

class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    dob = Column(String, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    alternate_phone = Column(String(15))
    email = Column(String, nullable=False)
    city = Column(String, nullable=False)
    blood_group = Column(String)

    primary_service_category = Column(String)
    experience_years = Column(Integer)
    experience_months = Column(Integer)

    aadhar_number = Column(String)
    pan_number = Column(String)
    electricity_bill_url = Column(String)
    profile_photo_url = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending")
    religion = Column(String, default="God knows")

    # Relationships
    addresses = relationship("Address", back_populates="worker", cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContact", back_populates="worker", cascade="all, delete-orphan")
    references = relationship("LocalReference", back_populates="worker", cascade="all, delete-orphan")
    employers = relationship("PreviousEmployer", back_populates="worker", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="worker", cascade="all, delete-orphan")
    bank_details = relationship("BankDetails", back_populates="worker", uselist=False, cascade="all, delete-orphan")
    police_verification = relationship("PoliceVerification", back_populates="worker", uselist=False, cascade="all, delete-orphan")
    references = relationship("LocalReference", back_populates="worker", cascade="all, delete-orphan")
    employers = relationship("PreviousEmployer", back_populates="worker", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="worker", cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    type = Column(String)  # 'permanent' or 'current'
    line1 = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    worker = relationship("Worker", back_populates="addresses")
    
class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    name = Column(String)
    relation = Column(String)
    phone = Column(String)

    worker = relationship("Worker", back_populates="emergency_contacts")
    
class BankDetails(Base):
    __tablename__ = "bank_details"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    ifsc_code = Column(String)
    account_number = Column(String)
    bank_name = Column(String)

    worker = relationship("Worker", back_populates="bank_details")
    
class PoliceVerification(Base):
    __tablename__ = "police_verification"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    status = Column(String)
    document_url = Column(String)
    verification_date = Column(String)
    remarks = Column(String)

    worker = relationship("Worker", back_populates="police_verification")

class LocalReference(Base):
    __tablename__ = "local_references"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    worker = relationship("Worker", back_populates="references")
    
class PreviousEmployer(Base):
    __tablename__ = "previous_employers"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    company_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    duration = Column(String, nullable=False)

    worker = relationship("Worker", back_populates="employers")

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    degree = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    year_of_passing = Column(String, nullable=False)

    worker = relationship("Worker", back_populates="education")


    
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
class AdditionalCategoryEnum(str, enum.Enum):
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
    image = Column(String, nullable=True)

    
    # Can store comma-separated features or JSON string
    
    duration = Column(Float, nullable=False)  # months or days?
    
    food_type = Column(Enum(FoodTypeEnum), nullable=True)
    is_popular = Column(Boolean, default=False)
    

ist = pytz.timezone("Asia/Kolkata")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index = True)
    uid = Column(String, unique = True, nullable = False)
    name = Column(String, nullable=False)
    phone = Column(String(15), nullable=False, unique=True)
    email = Column(String, nullable = True)
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
    email = Column(String, nullable = True)
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
    category = Column(Enum(AdditionalCategoryEnum), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    
    
class Categories(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, nullable=False)
    service_id = Column(String, nullable=False)
    image = Column(String, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(ist))
    
class Otp(Base):
    __tablename__ = "otps"
    
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())

class Testimonials(Base):
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, nullable=False)
    image_or_video = Column(String, nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(ist))