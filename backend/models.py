from db import Base
from sqlalchemy import Integer, Column, String, Float

class V_Breakfast_Lunch(Base):
    __tablename__ = "Veg_Breakfast_Lunch"

    id = Column(Integer, primary_key=True, index=True)
    food_type = Column(String, default="Veg")  # constant for this sheet
    plan_type = Column(String, index=True)     # Basic, Standard, Premium
    num_people = Column(Integer, index=True)   
    meal_combo = Column(String, nullable=False)
    frequency = Column(String)
    duration = Column(String)
    price = Column(Float)

