from database import Base
from sqlalchemy import (
    Column,
    LargeBinary,
    Integer,
    Float,
    String,
    DateTime,
    Enum,
    Text,
    Boolean,
    ForeignKey,
    Numeric,
    Table,
)
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
import pytz
import enum


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    dob = Column(String, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    alternate_phone = Column(String(15))
    email = Column(String, nullable=False)
    city = Column(String, nullable=False)
    blood_group = Column(String)

    primary_service_category = Column(ARRAY(String))
    experience_years = Column(Integer)
    experience_months = Column(Integer)
    languages_spoken = Column(ARRAY(String))
    availability = Column(ARRAY(String))

    aadhar_number = Column(String)
    pan_number = Column(String)
    electricity_bill_url = Column(String, nullable = True)
    profile_photo_url = Column(String, nullable = True)
    live_capture_url = Column(String, nullable = True)
    photoshoot_url = Column(String, nullable = True)

    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending")
    religion = Column(String, default="Any")
    
    bio = Column(Text, nullable = True)

    # Relationships
    addresses = relationship("Address", back_populates="worker", cascade="all, delete-orphan")
    emergency_contacts = relationship("EmergencyContact", back_populates="worker", cascade="all, delete-orphan")
    references = relationship("LocalReference", back_populates="worker", cascade="all, delete-orphan")
    employers = relationship("PreviousEmployer", back_populates="worker", cascade="all, delete-orphan")
    education = relationship("Education", back_populates="worker", cascade="all, delete-orphan")
    bank_details = relationship("BankDetails", back_populates="worker", uselist=False, cascade="all, delete-orphan")
    police_verification = relationship("PoliceVerification", back_populates="worker", uselist=False, cascade="all, delete-orphan")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    type = Column(String)  # 'permanent' or 'current'
    line1 = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    worker = relationship("Worker", back_populates="addresses")
    
class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    name = Column(String)
    relation = Column(String)
    phone = Column(String)

    worker = relationship("Worker", back_populates="emergency_contacts")
    
class BankDetails(Base):
    __tablename__ = "bank_details"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    ifsc_code = Column(String)
    account_number = Column(String)
    bank_name = Column(String)

    worker = relationship("Worker", back_populates="bank_details")
    
class PoliceVerification(Base):
    __tablename__ = "police_verification"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    status = Column(String)
    document_url = Column(String)
    verification_date = Column(String)
    remarks = Column(String)

    worker = relationship("Worker", back_populates="police_verification")

class LocalReference(Base):
    __tablename__ = "local_references"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    name = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    worker = relationship("Worker", back_populates="references")
    
class PreviousEmployer(Base):
    __tablename__ = "previous_employers"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    company_name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    duration = Column(String, nullable=False)

    worker = relationship("Worker", back_populates="employers")

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    degree = Column(String, nullable=False)
    institution = Column(String, nullable=False)
    year_of_passing = Column(String, nullable=False)

    worker = relationship("Worker", back_populates="education")

