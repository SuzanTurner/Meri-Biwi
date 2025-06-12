from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import List, Optional

class WorkerBase(BaseModel):
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
        
        
class WorkerUpdate(BaseModel):
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
    category: CategoryEnum
    plan_type: PlanTypeEnum
    number_of: int
    basic_details: List[str]
    description: Optional[str] = None
    frequency: int
    duration: int
    is_popular: Optional[bool] = False
    basic_price: float

    food_type: Optional[FoodTypeEnum]



class ServiceUpdate(BaseModel):
    name: Optional[str]
    category: Optional[CategoryEnum]
    plan_type: Optional[PlanTypeEnum]
    number_of: Optional[int]
    basic_details: Optional[List[str]]
    description: Optional[str]
    frequency: Optional[int]
    duration: Optional[int]
    is_popular: Optional[bool]
    basic_price: Optional[float]

    food_type: Optional[FoodTypeEnum]

class ServiceOut(BaseModel):
    id: int
    name: str
    category: CategoryEnum
    plan_type: PlanTypeEnum
    number_of: int
    basic_details: List[str]
    description: Optional[str]
    frequency: int
    duration: int
    is_popular: bool
    basic_price: float

    food_type: Optional[FoodTypeEnum]
    class Config:
        orm_mode = True

class User(BaseModel):
    uid : str
    phone : str
    email : str
    password : str
    avatar : str
    otp_verified : bool
    fcm_token : str
    wallet : float
    status : bool
    address_line_1 : str
    address_line_2 : str
    city : str
    longitude : str
    latitude : str
    created_at : str
    updated_at : str
    
class UserLogin(BaseModel):
    email : str
    password : str
    
class UpdateUser(BaseModel):
    phone: Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    avatar : Optional[str] = None
    otp_verified : Optional[bool] = False
    wallet : Optional[float] = None
    status : Optional[bool] = False
    address_line_1 : Optional[str] = None
    address_line_2 : Optional[str] = None
    city : Optional[str] = None
    latitude : Optional[str] = None
    longitude : Optional[str] = None
    
class Admin(BaseModel):
    username : str
    email : str
    password : str
    full_name : str
    profile_image : str
    role : str
    status : bool
    created_at : str
    
class AdminLogin(BaseModel):
    email : str
    password : str
    
class UpdateAdmin(BaseModel):
    username : Optional[str] = None
    email : Optional[str] = None
    password : Optional[str] = None
    full_name : Optional[str] = None
    role : Optional[str] = None
    status : Optional[bool] = False
    created_at : Optional[str] = None             
    

class AdditionalFeatureCreate(BaseModel):
    name: str
    price: int
    category: CategoryEnum
    description: str


class AdditionalFeatureOut(BaseModel):
    id: int
    name: str
    price: float
    category: CategoryEnum
    description: str

    class Config:
        from_attributes = True  # Pydantic v2+ equivalent of orm_mode = True