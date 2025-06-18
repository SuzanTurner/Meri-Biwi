from sqlalchemy import Column, BigInteger, String, Integer, Boolean, Date, Time, Text, Numeric, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class CustomerBooking(Base):
    __tablename__ = "customer_bookings"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, nullable=False)
    dietary_preference = Column(String(10), nullable=False)  # 'veg' or 'non-veg'
    no_of_people = Column(Integer, nullable=False)
    meals_per_day = Column(Text, nullable=False)  # Could also use ARRAY or JSON if supported
    service_purpose = Column(String(20), nullable=False)  # 'daily', 'weekends', 'occasionally'
    kitchen_platform_cleaning = Column(Boolean, nullable=False, default=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    booking_date = Column(TIMESTAMP, nullable=False, server_default=func.now())

    worker_id_1 = Column(BigInteger, nullable=False)
    worker_id_2 = Column(BigInteger, nullable=False)

    package_id = Column(String(20), nullable=False)
    basic_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    status = Column(String(20), nullable=False, default="ongoing")  # 'ongoing', 'completed', 'cancelled'

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    

