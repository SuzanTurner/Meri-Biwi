from sqlalchemy import Column, String, Integer,TIMESTAMP, Float
from database import Base
from sqlalchemy.sql import func

class Phonepay(Base):
    __tablename__ = "phonepay"

    id = Column(Integer, primary_key= True, autoincrement= True)
    merchant_transaction_id = Column(String, nullable = False)
    amount = Column(Float, nullable = False)
    status = Column(String, nullable = False)
    user_id = Column(Integer, nullable = False, index = True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate= func.now())
