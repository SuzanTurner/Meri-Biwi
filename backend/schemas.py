from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal

class AdditionalServiceBase(BaseModel):
    code: str
    name: str
    is_percentage: bool
    food_type: str
    plan_type: str
    meal_combo: str
    price_1: Optional[Decimal] = None
    price_2: Optional[Decimal] = None
    price_3: Optional[Decimal] = None
    price_4: Optional[Decimal] = None
    price_5: Optional[Decimal] = None
    price_6: Optional[Decimal] = None
    price_7: Optional[Decimal] = None

class AdditionalService(AdditionalServiceBase):
    id: int

    class Config:
        from_attributes = True

class MealBase(BaseModel):
    food_type: str
    plan_type: str
    num_people: int
    basic_price: Decimal
    basic_details: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None

class Meal(MealBase):
    id: int
    additional_services: List[AdditionalService] = []

    class Config:
        from_attributes = True 