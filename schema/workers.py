from pydantic import BaseModel, Field
from typing import List, Optional, Union


class BankDetails(BaseModel):
    ifsc_code: str = Field(..., alias="ifscCode")
    account_number: str = Field(..., alias="accountNumber")
    bank_name: str = Field(..., alias="bankName")


class PoliceVerification(BaseModel):
    status: str
    document_url: str = Field(..., alias="documentUrl")
    verification_date: str = Field(..., alias="verificationDate")
    remarks: str


class Address(BaseModel):
    line1: str
    city: str
    state: str
    zip_code: str = Field(..., alias="zipCode")


class EmergencyContact(BaseModel):
    name: str
    relation: str
    phone: str


class Reference(BaseModel):
    name: str
    relation: str
    phone: str


class Employer(BaseModel):
    company_name: str = Field(..., alias="companyName")
    position: str
    duration: str


class Education(BaseModel):
    degree: str
    institution: str
    year_of_passing: str = Field(..., alias="yearOfPassing")

class WorkExperience(BaseModel):
    years: int
    months: int


class WorkerRegisterRequest(BaseModel):
    full_name: str = Field(..., alias="fullName")
    gender: str
    age: int
    dob : str
    phone: str
    alternate_phone: str = Field(..., alias="alternateMobile")
    email: str
    city: str
    blood_group: str = Field(..., alias="bloodGroup")
    primary_service_category: List[str] = Field(..., alias="primaryServiceCategory")
    work_experience: WorkExperience = Field(..., alias="workExperience")
    languages_spoken: List[str] = Field(..., alias="languagesSpoken")
    availability: List[str]
    aadhar_number: str = Field(..., alias="aadharNumber")
    pan_number: str = Field(..., alias="panNumber")
    status: str = "Pending"
    religion: Optional[str] = "any"
    bio: Optional[str] = "string"
    addresses: List[Address]
    emergency_contacts: List[EmergencyContact] = Field(..., alias="emergencyContacts")
    references: List[Reference] = Field(..., alias="localReferences")
    employers: List[Employer] = Field(..., alias="previousEmployer")
    education: List[Education]
    bank_details: BankDetails = Field(..., alias="bankDetails")
    police_verification: PoliceVerification = Field(..., alias="policeVerification")

    class Config:
        allow_population_by_field_name = True
        from_attributes = True
        allow_population_by_alias = True
        populate_by_name = True
