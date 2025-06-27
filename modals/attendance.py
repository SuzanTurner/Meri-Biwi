from database import Base
from sqlalchemy import Column, String, Integer, Date, Boolean, TIMESTAMP, ForeignKey, Identity
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from modals.bookings import Booking
from modals.workers import Worker

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, Identity(), primary_key= True, )

    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)

    attendance_date = Column(Date, nullable = False)
    status = Column(Boolean, nullable = False)
    checkin_time = Column(String, nullable = True)
    checkout_time = Column(String, nullable = True)
    notes = Column(String, nullable = True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    booking = relationship("Booking", back_populates="attendances")
    worker = relationship("Worker", back_populates="attendances")




