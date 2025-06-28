from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable = False)
    msg = Column(String, nullable = False)
    msg_type = Column(String, nullable = True)
    created_at = Column(TIMESTAMP, server_default=func.now())