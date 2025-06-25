from sqlalchemy import Column, String, Integer, TIMESTAMP, Float
from sqlalchemy.sql import func
from database import Base

class Areas(Base):
    __tablename__ = "areas"
    
    id = Column(Integer, primary_key = True, autoincrement = True)
    
    area_name = Column(String, nullable = False)
    latitude = Column(Float)
    longitude = Column(Float)
    pincode = Column(Integer, nullable = True)
    landmark = Column(String, nullable = True)
    
    # created_at = Column(TIMESTAMP, server_default=func.now())
    # updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())