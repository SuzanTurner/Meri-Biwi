from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional

class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    city: str
    gender: str
    dob: str

    service: str
    exp: int
    availability: str
    id_proof: str
    id_proof_number: str
    about: str

    photo_path: str
    file_path: str
    created_at: datetime
    status : str
    
    religion : str

    class Config:
        orm_mode = True
        
        
class UserUpdate(BaseModel):
    status: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None

    service: Optional[str] = None
    exp: Optional[int] = None
    availability: Optional[str] = None
    id_proof: Optional[str] = None
    id_proof_number: Optional[int] = None
    about: Optional[str] = None

    photo_path: Optional[str] = None
    file_path: Optional[str] = None
    status : Optional[str] = None
    
    religion : Optional[str] = None
    
# class showuser(BaseModel):
#     name : str
#     phone : str
#     gender : str
#     service : str
#     status : str
    
#     class Config:
#         orm_mode = True
    

class UserCreate(UserBase):
    pass

class User(BaseModel):
    username : str
    password : str

class Login(BaseModel):
    username : str
    password : str

class FoodTypeEnum(str, Enum):
    veg = "Veg"
    non_veg = "Non-veg"


class PlanTypeEnum(str, Enum):
    basic = "basic"
    standard = "standard"
    premium = "premium"


class CategoryEnum(str, Enum):
    cleaning = "cleaning"
    cooking = "cooking"
    baby_care = "baby_care"
    elder_care = "elder_care"


class ServiceCreate(BaseModel):
    name: str
    food_type: FoodTypeEnum
    category: CategoryEnum
    plan_type: PlanTypeEnum
    number_of_people: int
    basic_details: List[str]
    description: Optional[str] = None
    frequency: int
    duration: int
    is_popular: Optional[bool] = False
    basic_price: float
    additional_feature_ids: Optional[List[int]] = None




class ServiceUpdate(BaseModel):
    name: Optional[str]
    food_type: Optional[FoodTypeEnum]
    category: Optional[CategoryEnum]
    plan_type: Optional[PlanTypeEnum]
    number_of_people: Optional[int]
    basic_details: Optional[List[str]]
    description: Optional[str]
    frequency: Optional[int]
    duration: Optional[int]
    is_popular: Optional[bool]
    basic_price: Optional[float]
    additional_feature_ids: Optional[List[int]] = None


class ServiceOut(BaseModel):
    id: int
    name: str
    food_type: FoodTypeEnum
    category: CategoryEnum
    plan_type: PlanTypeEnum
    number_of_people: int
    basic_details: List[str]
    description: Optional[str]
    frequency: int
    duration: int
    is_popular: bool
    basic_price: float
    additional_feature_ids: List[int] = []

    class Config:
        orm_mode = True
class AdditionalFeatureCreate(BaseModel):
    name: str
    price: int
    comments: Optional[str] = None


class AdditionalFeatureOut(BaseModel):
    id: int
    name: str
    price: float
    comments: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2+ equivalent of orm_mode = True