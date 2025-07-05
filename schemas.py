from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from typing import List, Optional

from decimal import Decimal


# class AddressBase(BaseModel):
#     type: str  # 'permanent' or 'current'
#     line1: str
#     city: str
#     state: str
#     zip_code: str

# class EmergencyContactBase(BaseModel):
#     name: str
#     relation: str
#     phone: str

# class BankDetailsBase(BaseModel):
#     ifsc_code: str
#     account_number: str
#     bank_name: str

# class PoliceVerificationBase(BaseModel):
#     status: str
#     document_url: str
#     verification_date: str
#     remarks: Optional[str] = None

# class LocalReferenceBase(BaseModel):
#     name: str
#     relation: str
#     phone: str

# class PreviousEmployerBase(BaseModel):
#     company_name: str
#     position: str
#     duration: str

# class EducationBase(BaseModel):
#     degree: str
#     institution: str
#     year_of_passing: str

# # Create schemas for related models
# class AddressCreate(AddressBase):
#     pass

# class EmergencyContactCreate(EmergencyContactBase):
#     pass

# class BankDetailsCreate(BankDetailsBase):
#     pass

# class PoliceVerificationCreate(PoliceVerificationBase):
#     pass

# class LocalReferenceCreate(LocalReferenceBase):
#     pass

# class PreviousEmployerCreate(PreviousEmployerBase):
#     pass

# class EducationCreate(EducationBase):
#     pass

# class WorkExperienceBase(BaseModel):
#     years: int
#     months: int

# class WorkExperienceCreate(WorkExperienceBase):
#     pass

# # Response schemas for related models
# class Address(AddressBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# class EmergencyContact(EmergencyContactBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# class BankDetails(BankDetailsBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# class PoliceVerification(PoliceVerificationBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# class LocalReference(LocalReferenceBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# class PreviousEmployer(PreviousEmployerBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# class Education(EducationBase):
#     id: int
#     worker_id: int

#     model_config = ConfigDict(from_attributes=True)

# # Worker schemas
# class WorkerBase(BaseModel):
#     full_name: str
#     gender: str
#     age: int
#     dob: str
#     phone: str
#     alternate_phone: Optional[str] = None
#     email: EmailStr
#     city: str
#     blood_group: Optional[str] = None
#     primary_service_category: str
#     experience_years: int
#     experience_months: int
#     languages_spoken: List[str]
#     availability: List[str]
#     preferred_community: List[str]
#     aadhar_number: str
#     pan_number: str
#     status: str = "Pending"
#     religion: str = "God knows"
    
#     model_config = ConfigDict(from_attributes=True)

# class WorkerCreate(WorkerBase):
#     profile_photo: Optional[UploadFile] = None
#     electricity_bill: Optional[UploadFile] = None
#     live_capture: Optional[UploadFile] = None
#     photoshoot: Optional[UploadFile] = None
#     permanent_address: Optional[AddressCreate] = None
#     current_address: Optional[AddressCreate] = None
#     emergency_contacts: Optional[List[EmergencyContactCreate]] = None
#     bank_details: Optional[BankDetailsCreate] = None
#     police_verification: Optional[PoliceVerificationCreate] = None
#     local_references: Optional[List[LocalReferenceCreate]] = None
#     previous_employers: Optional[List[PreviousEmployerCreate]] = None
#     education: Optional[List[EducationCreate]] = None

# class Worker(WorkerBase):
#     id: int
#     profile_photo_url: Optional[str] = None
#     electricity_bill_url: Optional[str] = None
#     live_capture_url: Optional[str] = None
#     photoshoot_url: Optional[str] = None
#     created_at: datetime
#     addresses: List[Address] = []
#     emergency_contacts: List[EmergencyContact] = []
#     bank_details: Optional[BankDetails] = None
#     police_verification: Optional[PoliceVerification] = None
#     local_references: List[LocalReference] = []
#     previous_employers: List[PreviousEmployer] = []
#     education: List[Education] = []

#     model_config = ConfigDict(from_attributes=True)

# Worker search response
# class WorkerSearchResponse(BaseModel):
#     status: str
#     count: int
#     workers: List[Worker]

# # Worker registration response
# class WorkerRegistrationResponse(BaseModel):
#     status: str
#     message: str
#     worker_id: int

# # Worker deletion response
# class WorkerDeletionResponse(BaseModel):
#     message: str

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
    image: Optional[str] = None
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
    image: Optional[str]

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
    image: Optional[str]

    food_type: Optional[FoodTypeEnum]
    
    model_config = ConfigDict(from_attributes=True)


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
    name : Optional[str] = None
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

    model_config = ConfigDict(from_attributes=True) 
        
class Categories(BaseModel):
    service_id: str
    image: str
    title: str
    categories : str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class otp(BaseModel):
    phone : str
    otp : str
    created_at : str
    
    
class Testimonials(BaseModel):
    image_or_video: str
    datatype : str
    title: str
    desciption : str
    categories : str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
        
class ServicePriceOut(BaseModel):
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
    image: Optional[str]

    food_type: Optional[FoodTypeEnum]
    additional_service: list[AdditionalFeatureOut]
    service_price: int
    additional_service_price: int
    total_price: int

    model_config = ConfigDict(from_attributes=True)

class Banner(BaseModel):
    image : str
    key : str
    url : str
    
# # Multipart Form Data Schemas for Worker Registration
# class WorkerMultipartForm(BaseModel):
#     # Basic worker information
#     full_name: str
#     gender: str
#     age: int
#     dob: str
#     phone: str
#     alternate_phone: Optional[str] = None
#     email: str
#     city: str
#     blood_group: Optional[str] = None
#     primary_service_category: str
#     experience_years: int
#     experience_months: int
#     languages_spoken: str  # JSON string
#     availability: str  # JSON string
#     preferred_community: str  # JSON string
#     aadhar_number: str
#     pan_number: str
#     status: str = "Pending"
#     religion: str = "God knows"
    
#     # File uploads
#     profile_photo: Optional[UploadFile] = None
#     electricity_bill: Optional[UploadFile] = None
#     live_capture: Optional[UploadFile] = None
#     photoshoot: Optional[UploadFile] = None
    
#     # Nested data as JSON strings
#     permanent_address: Optional[str] = None  # JSON string
#     current_address: Optional[str] = None  # JSON string
#     emergency_contacts: Optional[str] = None  # JSON string
#     bank_details: Optional[str] = None  # JSON string
#     police_verification: Optional[str] = None  # JSON string
#     local_references: Optional[str] = None  # JSON string
#     previous_employers: Optional[str] = None  # JSON string
#     education: Optional[str] = None  # JSON string


class CookingBooking(BaseModel):
    customer_id : str
    address_id : int
    
    service_purpose: Optional[str] = "cooking"
    meals_per_day: Optional[int] = None
    no_of_people: Optional[int] = None
    dietary_preference: Optional[str] = None
    kitchen_platform_cleaning: Optional[bool] = None
    
    package_id: Optional[str] = None
    basic_price: Optional[float] = None
    total_price: Optional[float] = None
    
    worker_id_1: Optional[int] = None
    worker_id_2: Optional[int] = None
    
    end_time: Optional[str] = None
    start_time: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # latitude: Optional[str]
    # longitude: Optional[str]
    # city: Optional[str]
    # address_line_1 : Optional[str]
    # address_line_2 : Optional[str]
    
    status: Optional[str] = "ongoing"

class CleaningBooking(BaseModel):
    customer_id: str
    address_id : int

    service_purpose: Optional[str] = "cleaning"
    
    no_of_floors: Optional[int]
    no_of_bathrooms: Optional[int]
    bhk: Optional[int]
    plan: Optional[str]  # daily, weekly, occasionally
    services: Optional[bool]

    start_date: Optional[str]
    end_date: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]

    worker_id_1: Optional[int]
    worker_id_2: Optional[int]

    package_id: Optional[str]
    basic_price: Optional[Decimal]
    total_price: Optional[Decimal]
    
    # latitude: Optional[str]
    # longitude: Optional[str]
    # city: Optional[str]
    # address_line_1 : Optional[str]
    # address_line_2 : Optional[str]

    status: Optional[str] = "ongoing"


class CreateBookingWithAddress(BaseModel):
    customer_id: str
    # start_date: Optional[str] = None
    # end_date: Optional[str] = None
    # start_time: Optional[str] = None
    # end_time: Optional[str] = None
    # worker_id_1: Optional[int] = None
    # worker_id_2: Optional[int] = None
    # package_id: Optional[str] = None
    # basic_price: Optional[Decimal] = None
    # total_price: Optional[Decimal] = None
    # status: Optional[str] = "ongoing"

    # Address fields
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    landmark: Optional[str] = None
    address_type: Optional[str] = None
    is_default: Optional[bool] = False

class Areas(BaseModel):
    area_name : str
    latitude : float
    longitude : float
    pincode : Optional[int] = None
    landmark : Optional[str] = None
    

    