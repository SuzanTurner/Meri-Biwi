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

    class Config:
        orm_mode = True
        
class showuser(BaseModel):
    name : str
    phone : str
    gender : str
    service : str
    status : str
    
    class Config:
        orm_mode = True
    

class UserCreate(UserBase):
    pass

class User(BaseModel):
    username : str
    password : str

class Login(BaseModel):
    username : str
    password : str

class CategoryEnum(str, Enum):
    cleaning = "cleaning"
    cooking = "cooking"
    baby_care = "Baby Care"
    elder_care = "Elder Care"
class ServiceBase(BaseModel):
    name: str
    category: CategoryEnum
    features: List[str]
    description: Optional[str] = None
    price: float
    duration: str
    is_popular: bool = False

class ServiceCreate(ServiceBase):
    pass

class ServiceOut(ServiceBase):
    id: int

    class Config:
        orm_mode = True
