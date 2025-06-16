from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Depends
from datetime import datetime
from database import get_db
from modals import Worker, Address, EmergencyContact, BankDetails, PoliceVerification, LocalReference, PreviousEmployer, Education
from sqlalchemy.orm import Session
from schemas import WorkerCreate, AddressCreate, EmergencyContactCreate, BankDetailsCreate, PoliceVerificationCreate, LocalReferenceCreate, PreviousEmployerCreate, EducationCreate
from sqlalchemy import or_
import shutil
import os
import dotenv
import re

dotenv.load_dotenv()
BASE_URL = os.getenv('BASE_URL')


router = APIRouter(
    tags = ["Workers"],
    prefix = '/workers'
)

UPLOAD_DIR = "uploads-workers"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")
DOCS_DIR = os.path.join(UPLOAD_DIR, "documents")

os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

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

@router.post("/")
async def register_worker(
    worker_data: WorkerCreate,
    db: Session = Depends(get_db)
):
    try:
        # Generate unique filenames for uploaded files
        photo_filename = None
        bill_filename = None
        full_url_photo = None
        full_url_bill = None
        
        if worker_data.profile_photo:
            
            safe_orig = re.sub(r'\s+', '_', worker_data.profile_photo.filename)
            photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            photo_path = os.path.join(PHOTOS_DIR, photo_filename)
            
            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(worker_data.profile_photo.file, buffer)
                
            public_url_photo = f"/uploads-workers/photos/{photo_filename}"
            full_url_photo = BASE_URL + public_url_photo
            # full_url = "http://127.0.0.1:8000" + public_url
        
        if worker_data.electricity_bill:
            safe_orig = re.sub(r'\s+', '_', worker_data.profile_photo.filename)
            bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            bill_path = os.path.join(DOCS_DIR, bill_filename)
            
            with open(bill_path, "wb") as buffer:
                shutil.copyfileobj(worker_data.electricity_bill.file, buffer)
            
            public_url_bill = f"/uploads-workers/documents/{bill_filename}"
            full_url_bill = BASE_URL + public_url_bill
            # full_url = "http://127.0.0.1:8000" + public_url
        
        try:
            # Create new worker record
            worker = Worker(
                full_name=worker_data.full_name,
                gender=worker_data.gender,
                age=worker_data.age,
                dob=worker_data.dob,
                phone=worker_data.phone,
                alternate_phone=worker_data.alternate_phone,
                email=worker_data.email,
                city=worker_data.city,
                blood_group=worker_data.blood_group,
                primary_service_category=worker_data.primary_service_category,
                experience_years=worker_data.experience_years,
                experience_months=worker_data.experience_months,
                languages_spoken=worker_data.languages_spoken,
                availability=worker_data.availability,
                preferred_community=worker_data.preferred_community,
                aadhar_number=worker_data.aadhar_number,
                pan_number=worker_data.pan_number,
                profile_photo_url=full_url_photo if photo_filename else None,
                electricity_bill_url=full_url_bill if bill_filename else None,
                status=worker_data.status,
                religion=worker_data.religion
            )
            db.add(worker)
            db.flush()  # Flush to get the worker ID
            
            # Add permanent address
            if worker_data.permanent_address:
                permanent_address = Address(
                    worker_id=worker.id,
                    type="permanent",
                    **worker_data.permanent_address.dict()
                )
                db.add(permanent_address)
            
            # Add current address
            if worker_data.current_address:
                current_address = Address(
                    worker_id=worker.id,
                    type="current",
                    **worker_data.current_address.dict()
                )
                db.add(current_address)
            
            # Add emergency contacts
            if worker_data.emergency_contacts:
                for contact in worker_data.emergency_contacts:
                    emergency_contact = EmergencyContact(
                        worker_id=worker.id,
                        **contact.dict()
                    )
                    db.add(emergency_contact)
            
            # Add bank details
            if worker_data.bank_details:
                bank_details = BankDetails(
                    worker_id=worker.id,
                    **worker_data.bank_details.dict()
                )
                db.add(bank_details)
            
            # Add police verification
            if worker_data.police_verification:
                police_verification = PoliceVerification(
                    worker_id=worker.id,
                    **worker_data.police_verification.dict()
                )
                db.add(police_verification)
            
            # Add local references
            if worker_data.local_references:
                for reference in worker_data.local_references:
                    local_reference = LocalReference(
                        worker_id=worker.id,
                        **reference.dict()
                    )
                    db.add(local_reference)
            
            # Add previous employers
            if worker_data.previous_employers:
                for employer in worker_data.previous_employers:
                    previous_employer = PreviousEmployer(
                        worker_id=worker.id,
                        **employer.dict()
                    )
                    db.add(previous_employer)
            
            # Add education records
            if worker_data.education:
                for edu in worker_data.education:
                    education = Education(
                        worker_id=worker.id,
                        **edu.dict()
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

@router.put("/{worker_id}")
async def update_worker(
    worker_id: int,
    worker_update: WorkerCreate,
    db: Session = Depends(get_db)
):
    try:
        # Get existing worker
        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not worker:
            raise HTTPException(status_code=404, detail=f"Worker with ID {worker_id} not found")

        # Update basic worker information
        update_data = worker_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            if hasattr(worker, key) and key not in ['profile_photo', 'electricity_bill', 'permanent_address', 
                                                   'current_address', 'emergency_contacts', 'bank_details', 
                                                   'police_verification', 'local_references', 'previous_employers', 
                                                   'education']:
                setattr(worker, key, value)

        # Handle file uploads
        if worker_update.profile_photo:
            # Delete old photo if exists
            if worker.profile_photo_url and os.path.exists(worker.profile_photo_url):
                os.remove(worker.profile_photo_url)
                
            safe_orig = re.sub(r'\s+', '_', worker_update.profile_photo.filename)
            photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            
            # photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{worker_update.profile_photo.filename}"
            photo_path = os.path.join(PHOTOS_DIR, photo_filename)
            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(worker_update.profile_photo.file, buffer)
                
            public_url_photo = f"/uploads-workers/photos/{photo_filename}"
            full_url_photo = BASE_URL + public_url_photo
            # full_url = "http://127.0.0.1:8000" + public_url
            
            worker.profile_photo_url = full_url_photo

        if worker_update.electricity_bill:
            # Delete old bill if exists
            
            if worker.electricity_bill_url and os.path.exists(worker.electricity_bill_url):
                os.remove(worker.electricity_bill_url)
            
            safe_orig = re.sub(r'\s+', '_', worker_update.electricity_bill.filename)
            bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            
            # bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{worker_update.electricity_bill.filename}"
            bill_path = os.path.join(DOCS_DIR, bill_filename)
            with open(bill_path, "wb") as buffer:
                shutil.copyfileobj(worker_update.electricity_bill.file, buffer)
                
            public_url_bill = f"/uploads-workers/documents/{bill_filename}"
            full_url_bill = BASE_URL + public_url_bill
            # full_url = "http://127.0.0.1:8000" + public_url
            
            worker.electricity_bill_url = full_url_bill

        # Handle addresses
        if worker_update.permanent_address:
            # Delete existing permanent address
            db.query(Address).filter(Address.worker_id == worker_id, Address.type == "permanent").delete()
            # Add new permanent address
            permanent_address = Address(
                worker_id=worker_id,
                type="permanent",
                **worker_update.permanent_address.dict()
            )
            db.add(permanent_address)

        if worker_update.current_address:
            # Delete existing current address
            db.query(Address).filter(Address.worker_id == worker_id, Address.type == "current").delete()
            # Add new current address
            current_address = Address(
                worker_id=worker_id,
                type="current",
                **worker_update.current_address.dict()
            )
            db.add(current_address)

        # Handle emergency contacts
        if worker_update.emergency_contacts:
            # Delete existing emergency contacts
            db.query(EmergencyContact).filter(EmergencyContact.worker_id == worker_id).delete()
            # Add new emergency contacts
            for contact in worker_update.emergency_contacts:
                new_contact = EmergencyContact(
                    worker_id=worker_id,
                    **contact.dict()
                )
                db.add(new_contact)

        # Handle bank details
        if worker_update.bank_details:
            # Update or create bank details
            existing_bank = db.query(BankDetails).filter(BankDetails.worker_id == worker_id).first()
            if existing_bank:
                for key, value in worker_update.bank_details.dict(exclude_unset=True).items():
                    setattr(existing_bank, key, value)
            else:
                new_bank = BankDetails(
                    worker_id=worker_id,
                    **worker_update.bank_details.dict()
                )
                db.add(new_bank)

        # Handle police verification
        if worker_update.police_verification:
            # Update or create police verification
            existing_verification = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
            if existing_verification:
                for key, value in worker_update.police_verification.dict(exclude_unset=True).items():
                    setattr(existing_verification, key, value)
            else:
                new_verification = PoliceVerification(
                    worker_id=worker_id,
                    **worker_update.police_verification.dict()
                )
                db.add(new_verification)

        # Handle local references
        if worker_update.local_references:
            # Delete existing references
            db.query(LocalReference).filter(LocalReference.worker_id == worker_id).delete()
            # Add new references
            for reference in worker_update.local_references:
                new_reference = LocalReference(
                    worker_id=worker_id,
                    **reference.dict()
                )
                db.add(new_reference)

        # Handle previous employers
        if worker_update.previous_employers:
            # Delete existing employers
            db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == worker_id).delete()
            # Add new employers
            for employer in worker_update.previous_employers:
                new_employer = PreviousEmployer(
                    worker_id=worker_id,
                    **employer.dict()
                )
                db.add(new_employer)

        # Handle education records
        if worker_update.education:
            # Delete existing education records
            db.query(Education).filter(Education.worker_id == worker_id).delete()
            # Add new education records
            for edu in worker_update.education:
                new_edu = Education(
                    worker_id=worker_id,
                    **edu.dict()
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

@router.delete('/{id}')
async def delete_worker(id: int, db: Session = Depends(get_db)):
    user = db.query(Worker).filter(Worker.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user found with ID {id}")
    
    db.delete(user)
    db.commit()
    return {"message": f"Deleted user with ID {id}"}

