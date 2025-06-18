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

ist = pytz.timezone("Asia/Kolkata")

class Categories(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, nullable=False)
    service_id = Column(String, nullable=False)
    image = Column(String, nullable=False)
    title = Column(String, nullable=False)
    categories = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(ist))
    
    
class Testimonials(Base):
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, nullable=False)
    image_or_video = Column(String, nullable=False)
    datatype = Column(String, nullable = False)
    title = Column(String, nullable=False)
    description = Column(String)
    categories = Column(String)
    base_64 = Column(Text, nullable = False)
    created_at = Column(DateTime, default=lambda: datetime.now(ist))


class Banner(Base):
    __tablename__ = "banners"
    
    id = Column(Integer, primary_key= True, index = True)
    image = Column(String, nullable = False)
    key = Column(String, nullable = True)
    url = Column(String, nullable = True)
    