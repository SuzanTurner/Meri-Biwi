from sqlalchemy import Column, Integer,Float, String, DateTime, Boolean
from database import Base
from datetime import datetime
import pytz

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
    