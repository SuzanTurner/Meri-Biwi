from database import Base
from sqlalchemy import (
    Column,
    LargeBinary,
    Integer,
    Float,
    String,
    DateTime,
    Enum,
    Text,
    Boolean,
    ForeignKey,
    Numeric,
    Table,
)
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
import pytz
import enum


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
    image = Column(Text, nullable=True)

    
    # Can store comma-separated features or JSON string
    
    duration = Column(Float, nullable=False)  # months or days?
    
    food_type = Column(Enum(FoodTypeEnum), nullable=True)
    is_popular = Column(Boolean, default=False)
    
class AdditionalFeature(Base):
    __tablename__ = "service_additional_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(AdditionalCategoryEnum), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    