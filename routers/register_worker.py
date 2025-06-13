from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Depends
from datetime import datetime
from database import get_db
from modals import Worker, Address, EmergencyContact, BankDetails, PoliceVerification, LocalReference, PreviousEmployer, Education
from sqlalchemy.orm import Session
from schemas import WorkerCreate, AddressCreate, EmergencyContactCreate, BankDetailsCreate, PoliceVerificationCreate, LocalReferenceCreate, PreviousEmployerCreate, EducationCreate
from sqlalchemy import or_
import shutil
import os

router = APIRouter(
    tags = ["Workers"]
)

UPLOAD_DIR = "uploads"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")
DOCS_DIR = os.path.join(UPLOAD_DIR, "documents")

os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

@router.get("/search-workers")
async def search_workers(name: str = None):
    try:
        db = next(get_db())
        
        if name:
            workers = db.query(Worker).filter(
                or_(
                    Worker.full_name.ilike(f"%{name}%"),
                    Worker.email.ilike(f"%{name}%"),
                    Worker.city.ilike(f"%{name}%")
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

@router.post("/register-worker")
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
    aadhar_number: str = Form(...),
    pan_number: str = Form(...),
    profile_photo: UploadFile = File(...),
    electricity_bill: UploadFile = File(...),
    status: str = "Pending",
    religion: str = "God knows"
):
    try:
        # Generate unique filenames
        photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{profile_photo.filename}"
        bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{electricity_bill.filename}"
        
        # Save files
        photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        bill_path = os.path.join(DOCS_DIR, bill_filename)
        
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(profile_photo.file, buffer)
        
        with open(bill_path, "wb") as buffer:
            shutil.copyfileobj(electricity_bill.file, buffer)
        
        # Create database session
        db = next(get_db())
        
        try:
            # Create new worker record
            worker = Worker(
                full_name=full_name,
                gender=gender,
                age=age,
                dob=dob,
                phone=phone,
                alternate_phone=alternate_phone,
                email=email,
                city=city,
                blood_group=blood_group,
                primary_service_category=primary_service_category,
                experience_years=experience_years,
                experience_months=experience_months,
                aadhar_number=aadhar_number,
                pan_number=pan_number,
                profile_photo_url=photo_path,
                electricity_bill_url=bill_path,
                status=status,
                religion=religion
            )
            db.add(worker)
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
            if os.path.exists(photo_path):
                os.remove(photo_path)
            if os.path.exists(bill_path):
                os.remove(bill_path)
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/all')
async def get_user(db: Session = Depends(get_db)):
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

@router.put("/update-worker/{worker_id}")
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
            if hasattr(worker, key):
                setattr(worker, key, value)

        # Handle related models if provided
        if worker_update.addresses:
            # Delete existing addresses
            db.query(Address).filter(Address.worker_id == worker_id).delete()
            # Add new addresses
            for address in worker_update.addresses:
                new_address = Address(**address.dict(), worker_id=worker_id)
                db.add(new_address)

        if worker_update.emergency_contacts:
            # Delete existing emergency contacts
            db.query(EmergencyContact).filter(EmergencyContact.worker_id == worker_id).delete()
            # Add new emergency contacts
            for contact in worker_update.emergency_contacts:
                new_contact = EmergencyContact(**contact.dict(), worker_id=worker_id)
                db.add(new_contact)

        if worker_update.bank_details:
            # Update or create bank details
            existing_bank = db.query(BankDetails).filter(BankDetails.worker_id == worker_id).first()
            if existing_bank:
                for key, value in worker_update.bank_details.dict(exclude_unset=True).items():
                    setattr(existing_bank, key, value)
            else:
                new_bank = BankDetails(**worker_update.bank_details.dict(), worker_id=worker_id)
                db.add(new_bank)

        if worker_update.police_verification:
            # Update or create police verification
            existing_verification = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
            if existing_verification:
                for key, value in worker_update.police_verification.dict(exclude_unset=True).items():
                    setattr(existing_verification, key, value)
            else:
                new_verification = PoliceVerification(**worker_update.police_verification.dict(), worker_id=worker_id)
                db.add(new_verification)

        if worker_update.references:
            # Delete existing references
            db.query(LocalReference).filter(LocalReference.worker_id == worker_id).delete()
            # Add new references
            for reference in worker_update.references:
                new_reference = LocalReference(**reference.dict(), worker_id=worker_id)
                db.add(new_reference)

        if worker_update.employers:
            # Delete existing employers
            db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == worker_id).delete()
            # Add new employers
            for employer in worker_update.employers:
                new_employer = PreviousEmployer(**employer.dict(), worker_id=worker_id)
                db.add(new_employer)

        if worker_update.education:
            # Delete existing education records
            db.query(Education).filter(Education.worker_id == worker_id).delete()
            # Add new education records
            for edu in worker_update.education:
                new_edu = Education(**edu.dict(), worker_id=worker_id)
                db.add(new_edu)

        # Handle file uploads if provided
        if worker_update.profile_photo:
            # Delete old photo if exists
            if worker.profile_photo_url and os.path.exists(worker.profile_photo_url):
                os.remove(worker.profile_photo_url)
            
            # Save new photo
            photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{worker_update.profile_photo.filename}"
            photo_path = os.path.join(PHOTOS_DIR, photo_filename)
            with open(photo_path, "wb") as buffer:
                shutil.copyfileobj(worker_update.profile_photo.file, buffer)
            worker.profile_photo_url = photo_path

        if worker_update.electricity_bill:
            # Delete old bill if exists
            if worker.electricity_bill_url and os.path.exists(worker.electricity_bill_url):
                os.remove(worker.electricity_bill_url)
            
            # Save new bill
            bill_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{worker_update.electricity_bill.filename}"
            bill_path = os.path.join(DOCS_DIR, bill_filename)
            with open(bill_path, "wb") as buffer:
                shutil.copyfileobj(worker_update.electricity_bill.file, buffer)
            worker.electricity_bill_url = bill_path

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

@router.delete('/delete-worker/{id}')
async def delete_worker(id: int, db: Session = Depends(get_db)):
    user = db.query(Worker).filter(Worker.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user found with ID {id}")
    
    db.delete(user)
    db.commit()
    return {"message": f"Deleted user with ID {id}"}

