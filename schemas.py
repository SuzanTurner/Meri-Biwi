from pydantic import BaseModel
from datetime import datetime

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


    
