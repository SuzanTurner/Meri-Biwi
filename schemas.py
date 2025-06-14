from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import List, Optional

# Base schemas for related models
class AddressBase(BaseModel):
    type: str
    line1: str
    city: str
    state: str
    zip_code: str

class EmergencyContactBase(BaseModel):
    name: str
    relation: str
    phone: str

class BankDetailsBase(BaseModel):
    ifsc_code: str
    account_number: str
    bank_name: str

class PoliceVerificationBase(BaseModel):
    status: str
    document_url: str
    verification_date: str
    remarks: Optional[str] = None

class LocalReferenceBase(BaseModel):
    name: str
    relation: str
    phone: str

class PreviousEmployerBase(BaseModel):
    company_name: str
    position: str
    duration: str

class EducationBase(BaseModel):
    degree: str
    institution: str
    year_of_passing: str

# Create schemas for related models
class AddressCreate(AddressBase):
    pass

class EmergencyContactCreate(EmergencyContactBase):
    pass

class BankDetailsCreate(BankDetailsBase):
    pass

class PoliceVerificationCreate(PoliceVerificationBase):
    pass

class LocalReferenceCreate(LocalReferenceBase):
    pass

class PreviousEmployerCreate(PreviousEmployerBase):
    pass

class EducationCreate(EducationBase):
    pass

# Response schemas for related models
class Address(AddressBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

class EmergencyContact(EmergencyContactBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

class BankDetails(BankDetailsBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

class PoliceVerification(PoliceVerificationBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

class LocalReference(LocalReferenceBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

class PreviousEmployer(PreviousEmployerBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

class Education(EducationBase):
    id: int
    worker_id: int

    class Config:
        from_attributes = True

# Worker schemas
class WorkerBase(BaseModel):
    full_name: str
    gender: str
    age: int
    dob: str
    phone: str
    alternate_phone: Optional[str] = None
    email: EmailStr
    city: str
    blood_group: Optional[str] = None
    primary_service_category: str
    experience_years: int
    experience_months: int
    aadhar_number: str
    pan_number: str
    status: str = "Pending"
    religion: str = "God knows"
    
    class Config:
        orm_mode = True

class WorkerCreate(WorkerBase):
    pass

class Worker(WorkerBase):
    id: int
    profile_photo_url: Optional[str] = None
    electricity_bill_url: Optional[str] = None
    created_at: datetime
    addresses: List[Address] = []
    emergency_contacts: List[EmergencyContact] = []
    bank_details: Optional[BankDetails] = None
    police_verification: Optional[PoliceVerification] = None
    references: List[LocalReference] = []
    employers: List[PreviousEmployer] = []
    education: List[Education] = []

    class Config:
        from_attributes = True

# Worker search response
class WorkerSearchResponse(BaseModel):
    status: str
    count: int
    workers: List[Worker]

# Worker registration response
class WorkerRegistrationResponse(BaseModel):
    status: str
    message: str
    worker_id: int

# Worker deletion response
class WorkerDeletionResponse(BaseModel):
    message: str

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
    phone : str
    password : str
    
class UserCreate(BaseModel):
    name : str
    phone : str
    email: Optional[str]
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
        from_attributes = True  
        
class Categories(BaseModel):
    id: int
    service_id: str
    image: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True

class otp(BaseModel):
    phone : str
    otp : str
    created_at : str