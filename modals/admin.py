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
    

    # basic_price = Column(Float, nullable=False)
    