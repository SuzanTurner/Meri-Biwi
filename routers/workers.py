from fastapi import APIRouter, HTTPException, Form, Query, UploadFile, File, Depends, Query
from typing import List
from datetime import datetime
from database import get_db
from modals.workers import Worker, Address, EmergencyContact, BankDetails, PoliceVerification, LocalReference, PreviousEmployer, Education
from sqlalchemy.orm import Session
# from schemas import WorkerCreate, AddressCreate, EmergencyContactCreate, BankDetailsCreate, PoliceVerificationCreate, LocalReferenceCreate, PreviousEmployerCreate, EducationCreate, WorkerMultipartForm
from sqlalchemy import or_
from urllib.parse import quote
import shutil
import os
import dotenv
import re
import json


dotenv.load_dotenv()
BASE_URL = os.getenv('BASE_URL')


router = APIRouter(
    tags = ["Workers"],
    prefix = '/workers'
)

UPLOAD_DIR = "/app/data/uploads-workers"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")
DOCS_DIR = os.path.join(UPLOAD_DIR, "documents")
LIVE_CAPTURE_DIR = os.path.join(PHOTOS_DIR, "live-capture")
PHOTOSHOOT_DIR = os.path.join(PHOTOS_DIR, "photoshoot")

os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(LIVE_CAPTURE_DIR, exist_ok=True)
os.makedirs(PHOTOSHOOT_DIR, exist_ok=True)

@router.get("/{name}")
async def search_workers(name: str = None):
    try:
        db = next(get_db())
        
        if name:
            workers = db.query(Worker).filter(
                or_(
                    Worker.full_name.ilike(f"%{name}%"),
                    # Worker.email.ilike(f"%{name}%"),
                    # Worker.city.ilike(f"%{name}%")
                )
            ).all()
        else:
            workers = db.query(Worker).all()
        
        worker_list = []
        for worker in workers:
            worker_dict = {
                "id": worker.id,
                "full_name": worker.full_name,
                "gender": worker.gender,
                "age": worker.age,
                "dob": worker.dob,
                "phone": worker.phone,
                "alternate_phone": worker.alternate_phone,
                "email": worker.email,
                "city": worker.city,
                "blood_group": worker.blood_group,
                "primary_service_category": worker.primary_service_category,
                "experience_years": worker.experience_years,
                "experience_months": worker.experience_months,
                "aadhar_number": worker.aadhar_number,
                "pan_number": worker.pan_number,
                "electricity_bill_url": worker.electricity_bill_url,
                "profile_photo_url": worker.profile_photo_url,
                "live_capture_url": worker.live_capture_url,
                "photoshoot_url": worker.photoshoot_url,
                "created_at": worker.created_at.isoformat() if worker.created_at else None,
                "status": worker.status,
                "religion": worker.religion
            }
            worker_list.append(worker_dict)
        
        return {
            "status": "success",
            "count": len(worker_list),
            "workers": worker_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# List[str] = Query([]


@router.post("/")
async def register_worker(
    full_name: str = Form(...),
    gender: str = Form(...),
    age: int = Form(...),
    dob: str = Form(...),
    phone: str = Form(...),
    alternate_phone: str = Form(None),
    email: str = Form(...),
    city: str = Form(...),
    blood_group: str = Form(None),
    primary_service_category: str = Form(...),
    experience_years: int = Form(...),
    experience_months: int = Form(...),
    languages_spoken: str = Form(...),  # JSON string
    availability: str = Form(...),  # JSON string
    aadhar_number: str = Form(...),
    pan_number: str = Form(...),
    status: str = Form("Pending"),
    religion: str = Form("Any"),
    bio : str = Form(...),
    profile_photo: UploadFile = File(None),
    electricity_bill: UploadFile = File(None),
    live_capture: UploadFile = File(None),
    photoshoot: UploadFile = File(None),
    permanent_address: str = Form(None),  # JSON string
    current_address: str = Form(None),  # JSON string
    emergency_contacts: str = Form(None),  # JSON string
    bank_details: str = Form(None),  # JSON string
    police_verification: str = Form(None),  # JSON string
    local_references: str = Form(None),  # JSON string
    previous_employers: str = Form(None),  # JSON string
    education: str = Form(None),  # JSON string
    db: Session = Depends(get_db)
):
    try:
        # Helper function to safely parse JSON or return default
        def safe_json_parse(json_str, default_value):
            if not json_str or json_str.strip() == "" or json_str.lower() == "string":
                return default_value
            try:
                return json.loads(json_str)
            except (json.JSONDecodeError, ValueError):
                return default_value

        # Parse JSON strings to Python objects with safe parsing
        def parse_list_field(field_str):
            if not field_str or field_str.strip() == "" or field_str.lower() == "string":
                return []
            field_str = field_str.strip()
            # Try JSON first
            if (field_str.startswith('[') and field_str.endswith(']')):
                try:
                    return json.loads(field_str)
                except Exception:
                    pass
            # If comma present, split by comma
            if ',' in field_str:
                return [item.strip() for item in field_str.split(',') if item.strip()]
            # Otherwise, split by whitespace
            return [item.strip() for item in field_str.split() if item.strip()]

        langs_list = parse_list_field(languages_spoken)
        avail_list = parse_list_field(availability)
        service_list = parse_list_field(primary_service_category)
        
        permanent_address_data = safe_json_parse(permanent_address, None)
        current_address_data = safe_json_parse(current_address, None)
        emergency_contacts_data = safe_json_parse(emergency_contacts, [])
        bank_details_data = safe_json_parse(bank_details, None)
        police_verification_data = safe_json_parse(police_verification, None)
        local_references_data = safe_json_parse(local_references, [])
        previous_employers_data = safe_json_parse(previous_employers, [])
        education_data = safe_json_parse(education, [])

        # Generate unique filenames for uploaded files
        photo_filename = None
        bill_filename = None
        live_capture_filename = None
        photoshoot_filename = None
        full_url_photo = None
        full_url_bill = None
        full_url_live_capture = None
        full_url_photoshoot = None
        
        if profile_photo:
            safe_orig = re.sub(r'\s+', '_', profile_photo.filename)
            photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            photo_filename = quote(photo_filename)
            
            photo_path = os.path.join(PHOTOS_DIR, photo_filename)
            
            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(profile_photo.file, buffer)
                
            public_url_photo = f"/app/data/uploads-workers/photos/{photo_filename}"
            
            full_url_photo = BASE_URL + public_url_photo
        
        if electricity_bill:
            safe_orig = re.sub(r'\s+', '_', electricity_bill.filename)
            bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            bill_filename = quote(bill_filename)
            bill_path = os.path.join(DOCS_DIR, bill_filename)
            
            with open(bill_path, "wb") as buffer:
                shutil.copyfileobj(electricity_bill.file, buffer)
            
            public_url_bill = f"/app/data/uploads-workers/documents/{bill_filename}"
            full_url_bill = BASE_URL + public_url_bill
        
        if live_capture:
            safe_orig = re.sub(r'\s+', '_', live_capture.filename)
            live_capture_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            live_capture_filename = quote(live_capture_filename)
            live_capture_path = os.path.join(LIVE_CAPTURE_DIR, live_capture_filename)
            
            with open(live_capture_path, "wb") as buffer:
                shutil.copyfileobj(live_capture.file, buffer)
            
            public_url_live_capture = (
                f"/app/data/uploads-workers/photos/live-capture/{live_capture_filename}"
            )
            full_url_live_capture = BASE_URL + public_url_live_capture
        
        if photoshoot:
            safe_orig = re.sub(r'\s+', '_', photoshoot.filename)
            photoshoot_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            photoshoot_filename = quote(photoshoot_filename)
            photoshoot_path = os.path.join(PHOTOSHOOT_DIR, photoshoot_filename)
            
            with open(photoshoot_path, "wb") as buffer:
                shutil.copyfileobj(photoshoot.file, buffer)
            
            public_url_photoshoot = (
                f"/app/data/uploads-workers/photos/photoshoot/{photoshoot_filename}"
            )
            full_url_photoshoot = BASE_URL + public_url_photoshoot
        
        try:
            # Create new worker record
            worker = Worker(
                full_name=full_name,
                gender=gender.lower(),
                age=age,
                dob=dob,
                phone=phone,
                alternate_phone=alternate_phone,
                email=email,
                city=city,
                blood_group=blood_group,
                primary_service_category=service_list,
                experience_years=experience_years,
                experience_months=experience_months,
                languages_spoken=langs_list,
                availability=avail_list,
                bio = bio,
                aadhar_number=aadhar_number,
                pan_number=pan_number,
                profile_photo_url=full_url_photo if photo_filename else None,
                electricity_bill_url=full_url_bill if bill_filename else None,
                live_capture_url=full_url_live_capture if live_capture_filename else None,
                photoshoot_url=full_url_photoshoot if photoshoot_filename else None,
                status=status,
                religion=religion.lower()
            )
            db.add(worker)
            db.flush()  # Flush to get the worker ID
            
            # Add permanent address
            if permanent_address_data:
                permanent_address = Address(
                    worker_id=worker.id,
                    type="permanent",
                    **permanent_address_data
                )
                db.add(permanent_address)
            
            # Add current address
            if current_address_data:
                current_address = Address(
                    worker_id=worker.id,
                    type="current",
                    **current_address_data
                )
                db.add(current_address)
            
            # Add emergency contacts
            if emergency_contacts_data:
                for contact in emergency_contacts_data:
                    emergency_contact = EmergencyContact(
                        worker_id=worker.id,
                        **contact
                    )
                    db.add(emergency_contact)
            
            # Add bank details
            if bank_details_data:
                bank_details = BankDetails(
                    worker_id=worker.id,
                    **bank_details_data
                )
                db.add(bank_details)
            
            # Add police verification
            if police_verification_data:
                police_verification = PoliceVerification(
                    worker_id=worker.id,
                    **police_verification_data
                )
                db.add(police_verification)
            
            # Add local references
            if local_references_data:
                for reference in local_references_data:
                    local_reference = LocalReference(
                        worker_id=worker.id,
                        **reference
                    )
                    db.add(local_reference)
            
            # Add previous employers
            if previous_employers_data:
                for employer in previous_employers_data:
                    previous_employer = PreviousEmployer(
                        worker_id=worker.id,
                        **employer
                    )
                    db.add(previous_employer)
            
            # Add education records
            if education_data:
                for edu in education_data:
                    education = Education(
                        worker_id=worker.id,
                        **edu
                    )
                    db.add(education)
            
            db.commit()
            db.refresh(worker)
            
            return {
                "status": "success",
                "message": "Worker registration successful",
                "worker_id": worker.id
            }
            
        except Exception as e:
            # Rollback in case of error
            db.rollback()
            # Clean up uploaded files
            if photo_filename and os.path.exists(photo_path):
                os.remove(photo_path)
            if bill_filename and os.path.exists(bill_path):
                os.remove(bill_path)
            if live_capture_filename and os.path.exists(live_capture_path):
                os.remove(live_capture_path)
            if photoshoot_filename and os.path.exists(photoshoot_path):
                os.remove(photoshoot_path)
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/')
async def get_worker(db: Session = Depends(get_db)):
    try:
        workers = db.query(Worker).all()
        worker_list = []
        for worker in workers:
            worker_dict = {
                "id": worker.id,
                "full_name": worker.full_name,
                "gender": worker.gender,
                "age": worker.age,
                "dob": worker.dob,
                "phone": worker.phone,
                "alternate_phone": worker.alternate_phone,
                "email": worker.email,
                "city": worker.city,
                "blood_group": worker.blood_group,
                "primary_service_category": worker.primary_service_category,
                "experience_years": worker.experience_years,
                "experience_months": worker.experience_months,
                "aadhar_number": worker.aadhar_number,
                "pan_number": worker.pan_number,
                "profile_photo_url": worker.profile_photo_url,
                "electricity_bill_url": worker.electricity_bill_url,
                "live_capture_url": worker.live_capture_url,
                "photoshoot_url": worker.photoshoot_url,
                "created_at": worker.created_at.isoformat() if worker.created_at else None,
                "status": worker.status,
                "religion": worker.religion
            }
            worker_list.append(worker_dict)
        return worker_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get('/{worker_id}/details')
async def get_worker_details(worker_id: int, db: Session = Depends(get_db)):
    try:
        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail=f"Worker with ID {worker_id} not found")
        
        # Get all related data
        addresses = db.query(Address).filter(Address.worker_id == worker_id).all()
        emergency_contacts = db.query(EmergencyContact).filter(EmergencyContact.worker_id == worker_id).all()
        bank_details = db.query(BankDetails).filter(BankDetails.worker_id == worker_id).first()
        police_verification = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
        local_references = db.query(LocalReference).filter(LocalReference.worker_id == worker_id).all()
        previous_employers = db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == worker_id).all()
        education = db.query(Education).filter(Education.worker_id == worker_id).all()
        
        # Format addresses
        permanent_address = None
        current_address = None
        for addr in addresses:
            if addr.type == "permanent":
                permanent_address = {
                    "line1": addr.line1,
                    "city": addr.city,
                    "state": addr.state,
                    "zip_code": addr.zip_code
                }
            elif addr.type == "current":
                current_address = {
                    "line1": addr.line1,
                    "city": addr.city,
                    "state": addr.state,
                    "zip_code": addr.zip_code
                }
        
        # Format emergency contacts
        emergency_contacts_list = []
        for contact in emergency_contacts:
            emergency_contacts_list.append({
                "name": contact.name,
                "relation": contact.relation,
                "phone": contact.phone
            })
        
        # Format bank details
        bank_details_dict = None
        if bank_details:
            bank_details_dict = {
                "ifsc_code": bank_details.ifsc_code,
                "account_number": bank_details.account_number,
                "bank_name": bank_details.bank_name
            }
        
        # Format police verification
        police_verification_dict = None
        if police_verification:
            police_verification_dict = {
                "status": police_verification.status,
                "document_url": police_verification.document_url,
                "verification_date": police_verification.verification_date,
                "remarks": police_verification.remarks
            }
        
        # Format local references
        local_references_list = []
        for ref in local_references:
            local_references_list.append({
                "name": ref.name,
                "relation": ref.relation,
                "phone": ref.phone
            })
        
        # Format previous employers
        previous_employers_list = []
        for emp in previous_employers:
            previous_employers_list.append({
                "company_name": emp.company_name,
                "position": emp.position,
                "duration": emp.duration
            })
        
        # Format education
        education_list = []
        for edu in education:
            education_list.append({
                "degree": edu.degree,
                "institution": edu.institution,
                "year_of_passing": edu.year_of_passing
            })
        
        worker_details = {
            "id": worker.id,
            "full_name": worker.full_name,
            "gender": worker.gender,
            "age": worker.age,
            "dob": worker.dob,
            "phone": worker.phone,
            "alternate_phone": worker.alternate_phone,
            "email": worker.email,
            "city": worker.city,
            "blood_group": worker.blood_group,
            "primary_service_category": worker.primary_service_category,
            "experience_years": worker.experience_years,
            "experience_months": worker.experience_months,
            "languages_spoken": worker.languages_spoken,
            "availability": worker.availability,
            "aadhar_number": worker.aadhar_number,
            "pan_number": worker.pan_number,
            "profile_photo_url": worker.profile_photo_url,
            "electricity_bill_url": worker.electricity_bill_url,
            "live_capture_url": worker.live_capture_url,
            "photoshoot_url": worker.photoshoot_url,
            "created_at": worker.created_at.isoformat() if worker.created_at else None,
            "status": worker.status,
            "religion": worker.religion,
            "permanent_address": permanent_address,
            "current_address": current_address,
            "emergency_contacts": emergency_contacts_list,
            "bank_details": bank_details_dict,
            "police_verification": police_verification_dict,
            "local_references": local_references_list,
            "previous_employers": previous_employers_list,
            "education": education_list
        }
        
        return {
            "status": "success",
            "worker": worker_details
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.put("/{worker_id}")
async def update_worker(
    worker_id: int,
    # Basic worker fields
    full_name: str = Form(None),
    gender: str = Form(None),
    age: int = Form(None),
    dob: str = Form(None),
    phone: str = Form(None),
    alternate_phone: str = Form(None),
    email: str = Form(None),
    city: str = Form(None),
    blood_group: str = Form(None),
    primary_service_category: str = Form(None),
    experience_years: int = Form(None),
    experience_months: int = Form(None),
    languages_spoken: str = Form(None),  # JSON string
    availability: str = Form(None),  # JSON string 
    aadhar_number: str = Form(None),
    pan_number: str = Form(None),
    status: str = Form(None),
    religion: str = Form(None),
    
    # File uploads
    # profile_photo: UploadFile = File(None),
    # electricity_bill: UploadFile = File(None),
    # live_capture: UploadFile = File(None),
    # photoshoot: UploadFile = File(None),
    
    # Address fields (individual fields for permanent address)
    permanent_address_line1: str = Form(None),
    permanent_address_city: str = Form(None),
    permanent_address_state: str = Form(None),
    permanent_address_zip_code: str = Form(None),
    
    # Address fields (individual fields for current address)
    current_address_line1: str = Form(None),
    current_address_city: str = Form(None),
    current_address_state: str = Form(None),
    current_address_zip_code: str = Form(None),
    
    # Bank details fields (individual fields)
    bank_ifsc_code: str = Form(None),
    bank_account_number: str = Form(None),
    bank_name: str = Form(None),
    
    # Police verification fields (individual fields)
    police_status: str = Form(None),
    police_document_url: str = Form(None),
    police_verification_date: str = Form(None),
    police_remarks: str = Form(None),
    
    # Emergency contacts (JSON array for multiple contacts)
    emergency_contacts: str = Form(None),  # JSON string
    
    # Local references (JSON array for multiple references)
    local_references: str = Form(None),  # JSON string
    
    # Previous employers (JSON array for multiple employers)
    previous_employers: str = Form(None),  # JSON string
    
    # Education (JSON array for multiple education records)
    education: str = Form(None),  # JSON string
    
    db: Session = Depends(get_db)
):
    try:
        # Get existing worker
        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail=f"Worker with ID {worker_id} not found")

        # Parse JSON strings to Python objects
        try:
            # Helper function to safely parse JSON or return default
            def safe_json_parse(json_str, default_value):
                if not json_str or json_str.strip() == "" or json_str.lower() == "string":
                    return default_value
                try:
                    return json.loads(json_str)
                except (json.JSONDecodeError, ValueError):
                    return default_value

            languages_spoken_list = safe_json_parse(languages_spoken, None)
            availability_list = safe_json_parse(availability, None)
            
            emergency_contacts_data = safe_json_parse(emergency_contacts, None)
            local_references_data = safe_json_parse(local_references, None)
            previous_employers_data = safe_json_parse(previous_employers, None)
            education_data = safe_json_parse(education, None)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing form data: {str(e)}")

        # Update basic worker information with defensive checks
        def is_valid_update(val):
            return val is not None and (not isinstance(val, str) or (val.strip() != '' and val.lower() != 'string'))

        if is_valid_update(full_name):
            worker.full_name = full_name
        if is_valid_update(gender):
            worker.gender = gender
        if is_valid_update(age):
            worker.age = age
        if is_valid_update(dob):
            worker.dob = dob
        if is_valid_update(phone):
            worker.phone = phone
        if is_valid_update(alternate_phone):
            worker.alternate_phone = alternate_phone
        if is_valid_update(email):
            worker.email = email
        if is_valid_update(city):
            worker.city = city
        if is_valid_update(blood_group):
            worker.blood_group = blood_group
        if is_valid_update(primary_service_category):
            worker.primary_service_category = primary_service_category
        if is_valid_update(experience_years):
            worker.experience_years = experience_years
        if is_valid_update(experience_months):
            worker.experience_months = experience_months
        if languages_spoken_list is not None:
            worker.languages_spoken = languages_spoken_list
        if availability_list is not None:
            worker.availability = availability_list
        if is_valid_update(aadhar_number):
            worker.aadhar_number = aadhar_number
        if is_valid_update(pan_number):
            worker.pan_number = pan_number
        if is_valid_update(status):
            worker.status = status
        if is_valid_update(religion):
            worker.religion = religion

        # Handle file uploads
        # if profile_photo:
        #     # Delete old photo if exists
        #     if worker.profile_photo_url and os.path.exists(worker.profile_photo_url):
        #         os.remove(worker.profile_photo_url)
                
        #     safe_orig = re.sub(r'\s+', '_', profile_photo.filename)
        #     photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        #     photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        #     with open(photo_path, "wb") as buffer:
        #         shutil.copyfileobj(profile_photo.file, buffer)
                
        #     public_url_photo = f"/uploads-workers/photos/{photo_filename}"
        #     full_url_photo = BASE_URL + public_url_photo
        #     worker.profile_photo_url = full_url_photo

        # if electricity_bill:
        #     # Delete old bill if exists
        #     if worker.electricity_bill_url and os.path.exists(worker.electricity_bill_url):
        #         os.remove(worker.electricity_bill_url)
            
        #     safe_orig = re.sub(r'\s+', '_', electricity_bill.filename)
        #     bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        #     bill_path = os.path.join(DOCS_DIR, bill_filename)
        #     with open(bill_path, "wb") as buffer:
        #         shutil.copyfileobj(electricity_bill.file, buffer)
                
        #     public_url_bill = f"/uploads-workers/documents/{bill_filename}"
        #     full_url_bill = BASE_URL + public_url_bill
        #     worker.electricity_bill_url = full_url_bill

        # # Handle live capture upload
        # if live_capture:
        #     # Delete old live capture if exists
        #     if worker.live_capture_url and os.path.exists(worker.live_capture_url):
        #         os.remove(worker.live_capture_url)
            
        #     safe_orig = re.sub(r'\s+', '_', live_capture.filename)
        #     live_capture_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        #     live_capture_path = os.path.join(LIVE_CAPTURE_DIR, live_capture_filename)
            
        #     with open(live_capture_path, "wb") as buffer:
        #         shutil.copyfileobj(live_capture.file, buffer)
                
        #     public_url_live_capture = f"/uploads-workers/photos/live-capture/{live_capture_filename}"
        #     full_url_live_capture = BASE_URL + public_url_live_capture
        #     worker.live_capture_url = full_url_live_capture

        # # Handle photoshoot upload
        # if photoshoot:
        #     # Delete old photoshoot if exists
        #     if worker.photoshoot_url and os.path.exists(worker.photoshoot_url):
        #         os.remove(worker.photoshoot_url)
            
        #     safe_orig = re.sub(r'\s+', '_', photoshoot.filename)
        #     photoshoot_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        #     photoshoot_path = os.path.join(PHOTOSHOOT_DIR, photoshoot_filename)
            
        #     with open(photoshoot_path, "wb") as buffer:
        #         shutil.copyfileobj(photoshoot.file, buffer)
                
        #     public_url_photoshoot = f"/uploads-workers/photos/photoshoot/{photoshoot_filename}"
        #     full_url_photoshoot = BASE_URL + public_url_photoshoot
        #     worker.photoshoot_url = full_url_photoshoot

        # Handle permanent address (individual fields)
        if any([permanent_address_line1, permanent_address_city, permanent_address_state, permanent_address_zip_code]):
            existing_permanent = db.query(Address).filter(Address.worker_id == worker_id, Address.type == "permanent").first()
            if existing_permanent:
                # Update existing permanent address
                if permanent_address_line1 is not None:
                    existing_permanent.line1 = permanent_address_line1
                if permanent_address_city is not None:
                    existing_permanent.city = permanent_address_city
                if permanent_address_state is not None:
                    existing_permanent.state = permanent_address_state
                if permanent_address_zip_code is not None:
                    existing_permanent.zip_code = permanent_address_zip_code
            else:
                # Create new permanent address
                permanent_address = Address(
                    worker_id=worker_id,
                    type="permanent",
                    line1=permanent_address_line1 or "",
                    city=permanent_address_city or "",
                    state=permanent_address_state or "",
                    zip_code=permanent_address_zip_code or ""
                )
                db.add(permanent_address)

        # Handle current address (individual fields)
        if any([current_address_line1, current_address_city, current_address_state, current_address_zip_code]):
            existing_current = db.query(Address).filter(Address.worker_id == worker_id, Address.type == "current").first()
            if existing_current:
                # Update existing current address
                if current_address_line1 is not None:
                    existing_current.line1 = current_address_line1
                if current_address_city is not None:
                    existing_current.city = current_address_city
                if current_address_state is not None:
                    existing_current.state = current_address_state
                if current_address_zip_code is not None:
                    existing_current.zip_code = current_address_zip_code
            else:
                # Create new current address
                current_address = Address(
                    worker_id=worker_id,
                    type="current",
                    line1=current_address_line1 or "",
                    city=current_address_city or "",
                    state=current_address_state or "",
                    zip_code=current_address_zip_code or ""
                )
                db.add(current_address)

        # Handle bank details (individual fields)
        if any([bank_ifsc_code, bank_account_number, bank_name]):
            existing_bank = db.query(BankDetails).filter(BankDetails.worker_id == worker_id).first()
            if existing_bank:
                # Update existing bank details
                if bank_ifsc_code is not None:
                    existing_bank.ifsc_code = bank_ifsc_code
                if bank_account_number is not None:
                    existing_bank.account_number = bank_account_number
                if bank_name is not None:
                    existing_bank.bank_name = bank_name
            else:
                # Create new bank details
                new_bank = BankDetails(
                    worker_id=worker_id,
                    ifsc_code=bank_ifsc_code or "",
                    account_number=bank_account_number or "",
                    bank_name=bank_name or ""
                )
                db.add(new_bank)

        # Handle police verification (individual fields)
        if any([police_status, police_document_url, police_verification_date, police_remarks]):
            existing_verification = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
            if existing_verification:
                # Update existing police verification
                if police_status is not None:
                    existing_verification.status = police_status
                if police_document_url is not None:
                    existing_verification.document_url = police_document_url
                if police_verification_date is not None:
                    existing_verification.verification_date = police_verification_date
                if police_remarks is not None:
                    existing_verification.remarks = police_remarks
            else:
                # Create new police verification
                new_verification = PoliceVerification(
                    worker_id=worker_id,
                    status=police_status or "",
                    document_url=police_document_url or "",
                    verification_date=police_verification_date or "",
                    remarks=police_remarks or ""
                )
                db.add(new_verification)

        # Handle emergency contacts (JSON array - replace entire list)
        if emergency_contacts_data is not None:
            # Delete existing emergency contacts
            db.query(EmergencyContact).filter(EmergencyContact.worker_id == worker_id).delete()
            # Add new emergency contacts
            for contact in emergency_contacts_data:
                new_contact = EmergencyContact(
                    worker_id=worker_id,
                    **contact
                )
                db.add(new_contact)

        # Handle local references (JSON array - replace entire list)
        if local_references_data is not None:
            # Delete existing references
            db.query(LocalReference).filter(LocalReference.worker_id == worker_id).delete()
            # Add new references
            for reference in local_references_data:
                new_reference = LocalReference(
                    worker_id=worker_id,
                    **reference
                )
                db.add(new_reference)

        # Handle previous employers (JSON array - replace entire list)
        if previous_employers_data is not None:
            # Delete existing employers
            db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == worker_id).delete()
            # Add new employers
            for employer in previous_employers_data:
                new_employer = PreviousEmployer(
                    worker_id=worker_id,
                    **employer
                )
                db.add(new_employer)

        # Handle education records (JSON array - replace entire list)
        if education_data is not None:
            # Delete existing education records
            db.query(Education).filter(Education.worker_id == worker_id).delete()
            # Add new education records
            for edu in education_data:
                new_edu = Education(
                    worker_id=worker_id,
                    **edu
                )
                db.add(new_edu)
            
        try:
            db.commit()
            db.refresh(worker)
            return {
                "status": "success",
                "message": "Worker information updated successfully",
                "worker_id": worker.id
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
        
        
@router.put('/{worker_id}/docs')
async def update_worker_docs( worker_id : int,
    # File uploads
    profile_photo: UploadFile = File(None),
    electricity_bill: UploadFile = File(None),
    live_capture: UploadFile = File(None),
    photoshoot: UploadFile = File(None),
    db: Session = Depends(get_db)):
    
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail=f"Worker with ID {worker_id} not found")
    
    if profile_photo:
            # Delete old photo if exists
        if worker.profile_photo_url and os.path.exists(worker.profile_photo_url):
            os.remove(worker.profile_photo_url)
            
        safe_orig = re.sub(r'\s+', '_', profile_photo.filename)
        photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(profile_photo.file, buffer)
            
        public_url_photo = f"/uploads-workers/photos/{photo_filename}"
        full_url_photo = BASE_URL + public_url_photo
        worker.profile_photo_url = full_url_photo

    if electricity_bill:
        # Delete old bill if exists
        if worker.electricity_bill_url and os.path.exists(worker.electricity_bill_url):
            os.remove(worker.electricity_bill_url)
        
        safe_orig = re.sub(r'\s+', '_', electricity_bill.filename)
        bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        bill_path = os.path.join(DOCS_DIR, bill_filename)
        with open(bill_path, "wb") as buffer:
            shutil.copyfileobj(electricity_bill.file, buffer)
            
        public_url_bill = f"/uploads-workers/documents/{bill_filename}"
        full_url_bill = BASE_URL + public_url_bill
        worker.electricity_bill_url = full_url_bill

    # Handle live capture upload
    if live_capture:
        # Delete old live capture if exists
        if worker.live_capture_url and os.path.exists(worker.live_capture_url):
            os.remove(worker.live_capture_url)
        
        safe_orig = re.sub(r'\s+', '_', live_capture.filename)
        live_capture_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        live_capture_path = os.path.join(LIVE_CAPTURE_DIR, live_capture_filename)
        
        with open(live_capture_path, "wb") as buffer:
            shutil.copyfileobj(live_capture.file, buffer)
            
        public_url_live_capture = f"/uploads-workers/photos/live-capture/{live_capture_filename}"
        full_url_live_capture = BASE_URL + public_url_live_capture
        worker.live_capture_url = full_url_live_capture

    # Handle photoshoot upload
    if photoshoot:
        # Delete old photoshoot if exists
        if worker.photoshoot_url and os.path.exists(worker.photoshoot_url):
            os.remove(worker.photoshoot_url)
        
        safe_orig = re.sub(r'\s+', '_', photoshoot.filename)
        photoshoot_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        photoshoot_path = os.path.join(PHOTOSHOOT_DIR, photoshoot_filename)
        
        with open(photoshoot_path, "wb") as buffer:
            shutil.copyfileobj(photoshoot.file, buffer)
            
        public_url_photoshoot = f"/uploads-workers/photos/photoshoot/{photoshoot_filename}"
        full_url_photoshoot = BASE_URL + public_url_photoshoot
        worker.photoshoot_url = full_url_photoshoot
    
    return {"status" : "success", "message" : "worker docs updated"}
    
    

@router.delete('/{id}')
async def delete_worker(id: int, db: Session = Depends(get_db)):
    user = db.query(Worker).filter(Worker.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user found with ID {id}")
    
    db.delete(user)
    db.commit()
    return {"message": f"Deleted user with ID {id}"}

