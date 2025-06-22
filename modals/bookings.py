from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Text, Numeric, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, nullable=True)

    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    
    service_type = Column(String, nullable = False)

    booking_date = Column(TIMESTAMP, nullable=True, server_default=func.now())

    worker_id_1 = Column(BigInteger, nullable=True)
    worker_id_2 = Column(BigInteger, nullable=True)

    package_id = Column(String(20), nullable=True)
    basic_price = Column(Numeric(10, 2), nullable=True)
    total_price = Column(Numeric(10, 2), nullable=True)

    status = Column(String(20), nullable=True, default="ongoing")  # 'ongoing', 'completed', 'cancelled'

    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, server_default=func.now(), onupdate=func.now())
    
    cookings = relationship("Cooking", back_populates="booking", cascade="all, delete-orphan")
    cleanings = relationship("Cleaning", back_populates="booking", cascade="all, delete-orphan")
    addresses = relationship("CustomerAddress", back_populates="booking", cascade="all, delete-orphan")

    
class Cooking(Base):
    
    __tablename__ = "cooking_bookings"
    
    id = Column(Integer, primary_key=True, nullable = False)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    customer_id = Column(String, nullable=True)
    
    dietary_preference = Column(String(10), nullable=True) 
    no_of_people = Column(Integer, nullable=True)
    meals_per_day = Column(Text, nullable=True) 
    service_purpose = Column(String(20), nullable=True)  
    kitchen_platform_cleaning = Column(Boolean, nullable=True, default=False)    
    
    booking = relationship("Booking", back_populates="cookings")
    
    
class Cleaning(Base):
    
    __tablename__ = "cleaning_bookings"
    
    id = Column(Integer, primary_key=True, nullable = False)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    customer_id = Column(String, nullable=True)
        
    no_of_floors = Column(Integer, nullable=True) 
    no_of_bathrooms = Column(Integer, nullable=True)
    bhk = Column(Integer, nullable=True) 
    plan = Column(String(20), nullable=True)  # daily, weekly, occasionly
    services = Column(Boolean, nullable=True, default=False) # additional services
    
    booking = relationship("Booking", back_populates="cleanings")
    


class CustomerAddress(Base):
    __tablename__ = "customer_address"

    id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    customer_id = Column(String(100), nullable=False)

    address_line1 = Column(String(255), nullable=True)
    address_line2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    landmark = Column(String(255), nullable=True)

    address_type = Column(String, nullable=True)
    is_default = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, server_default=func.now(), onupdate=func.now())
    
    booking = relationship("Booking", back_populates="addresses")