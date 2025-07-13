from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Refund(Base):
    __tablename__ = 'refunds'

    refund_id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    booking_id = Column(Integer, ForeignKey("bookings.id"),  nullable=False)
    customer_id = Column(String, nullable=False) 

    # plan = Column(String, nullable = True)

    amount = Column(DECIMAL(10, 2), nullable=False)
    refund_status = Column(String(20), default='pending')  # pending, processed, failed
    payment_method = Column(String(50))
    cancellation_date = Column(DateTime, default=None)
    refund_date = Column(String, nullable = True, default = "Coming Soons")
    created_at = Column(DateTime, server_default=func.now())

    booking = relationship("Booking", back_populates="refunds")
