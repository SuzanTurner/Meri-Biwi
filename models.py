from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between meals and additional services
meal_services = Table(
    "meal_services",
    Base.metadata,
    Column("meal_id", Integer, ForeignKey("meals.id", ondelete="CASCADE")),
    Column("service_id", Integer, ForeignKey("additional_services.id", ondelete="CASCADE"))
)

class Meals(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)
    food_type = Column(String(20))
    plan_type = Column(String(20))
    num_people = Column(Integer)
    basic_price = Column(Numeric)
    basic_details = Column(Text)

    # Relationship to additional services
    additional_services = relationship(
        "AdditionalService",
        secondary=meal_services,
        back_populates="meals"
    )

class AdditionalService(Base):
    __tablename__ = "additional_services"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(5))
    name = Column(Text)
    is_percentage = Column(Boolean)
    food_type = Column(String(20))
    plan_type = Column(String(20))
    meal_combo = Column(String(40))
    price_1 = Column(Numeric)
    price_2 = Column(Numeric)
    price_3 = Column(Numeric)
    price_4 = Column(Numeric)
    price_5 = Column(Numeric)
    price_6 = Column(Numeric)
    price_7 = Column(Numeric)

    # Relationship to meals
    meals = relationship(
        "Meals",
        secondary=meal_services,
        back_populates="additional_services"
    )

cleaning_additional_plans = Table(
    "cleaning_additional_plans",
    Base.metadata,
    Column("cleaning_id", Integer, ForeignKey("cleaning.id", ondelete="CASCADE")),
    Column("additional_plan_id", Integer, ForeignKey("additional_cleaning.id", ondelete="CASCADE"))
)

class AdditionalCleaningPlan(Base):
    __tablename__ = "additional_cleaning"

    id = Column(Integer, primary_key=True, index=True)
    bathroom_1 = Column(Numeric)
    bathroom_2 = Column(Numeric)
    bathroom_3 = Column(Numeric)
    bathroom_4 = Column(Numeric)
    bathroom_5 = Column(Numeric)
    code = Column(String(5))
    service_name = Column(Text)
    plan = Column(String(20))
    floor = Column(Integer)

    cleanings = relationship(
        "Cleaning",
        secondary="cleaning_additional_plans",
        back_populates="additional_cleaning_plans"
    )

class Cleaning(Base):
    __tablename__ = "cleaning"

    id = Column(Integer, primary_key=True, index=True)
    floor = Column(Integer)
    plan = Column(String(20))
    bhk = Column(Integer)
    price = Column(Numeric)

    # Relationship to additional cleaning plans
    additional_cleaning_plans = relationship(
        "AdditionalCleaningPlan",
        secondary="cleaning_additional_plans",
        back_populates="cleanings"
    )
