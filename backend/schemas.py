from pydantic import BaseModel

class Veg_Breakfast_Lunch_Base(BaseModel):
    food_type : str
    plan_type : str   # Basic, Standard, Premium
    num_people : int
    meal_combo : str 
    frequency : str
    duration : str
    price : float

class Veg_Breakfast_Lunch_Create(Veg_Breakfast_Lunch_Base):
    pass

class Veg_Breakfast_Lunch(Veg_Breakfast_Lunch_Base):
    id : int

    class config():
        # orm = True  # if version < 2.x
        from_attribute = True