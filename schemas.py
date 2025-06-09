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
    

# class User(BaseModel):
#     username : str
#     password : str

# class Login(BaseModel):
#     username : str
#     password : str

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
    