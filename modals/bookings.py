from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Date, Time, Text, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class CustomerBooking(Base):
    __tablename__ = "customer_bookings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, nullable=True)
    dietary_preference = Column(String(10), nullable=True)  # 'veg' or 'non-veg'
    no_of_people = Column(Integer, nullable=True)
    meals_per_day = Column(Text, nullable=True)  # Could also use ARRAY or JSON if supported
    service_purpose = Column(String(20), nullable=True)  # 'daily', 'weekends', 'occasionally'
    kitchen_platform_cleaning = Column(Boolean, nullable=True, default=False)

    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)

    booking_date = Column(TIMESTAMP, nullable=True, server_default=func.now())

    worker_id_1 = Column(BigInteger, nullable=True)
    worker_id_2 = Column(BigInteger, nullable=True)

    package_id = Column(String(20), nullable=True)
    basic_price = Column(Numeric(10, 2), nullable=True)
    total_price = Column(Numeric(10, 2), nullable=True)

    status = Column(String(20), nullable=True, default="ongoing")  # 'ongoing', 'completed', 'cancelled'

    created_at = Column(TIMESTAMP, nullable=True, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, server_default=func.now(), onupdate=func.now())

    

