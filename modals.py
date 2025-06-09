from database import Base
from sqlalchemy import Column, Integer,Float, String, DateTime, Enum,Text,Boolean,Table,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

import enum
service_additional_feature_link = Table(
    "service_additional_feature_link",
    Base.metadata,  # Use Base.metadata if Base is declarative
    Column(
        "service_id", Integer, ForeignKey("services.id"), primary_key=True
    ),  # Added primary_key=True
    Column(
        "additional_feature_id",
        Integer,
        ForeignKey("service_additional_features.id"),
        primary_key=True,
    ),  # Added primary_key=True
)


class User(Base):
    __tablename__ = "users"

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
    baby_care = "Baby Care"
    elder_care = "Elder Care"
class FoodTypeEnum(str, enum.Enum):
    veg = "Veg"
    non_veg = "Non-veg"


class PlanTypeEnum(str, enum.Enum):
    basic = "basic"
    standard = "standard"
    premium = "premium"

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    food_type = Column(Enum(FoodTypeEnum), nullable=False)

    category = Column(Enum(CategoryEnum), nullable=False)
    plan_type = Column(Enum(PlanTypeEnum), nullable=False)
    number_of_people = Column(Integer, nullable=False)
    
    basic_details = Column(JSON, nullable=False)
    # Can store comma-separated features or JSON string
    description = Column(Text)
    
    frequency = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  # months or days?
    
    is_popular = Column(Boolean, default=False)

    basic_price = Column(Float, nullable=False)
    additional_features = relationship(
        "AdditionalFeature",
        secondary=service_additional_feature_link,  # Pass the Table object directly
        backref="services",
    )

class AdditionalFeature(Base):
    __tablename__ = "service_additional_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)