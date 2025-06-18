from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Otp(Base):
    __tablename__ = "otps"
    
    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    otp = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow())