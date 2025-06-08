from pydantic import BaseModel
from typing import List, Optional

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
    
    