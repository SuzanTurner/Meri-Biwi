from fastapi import APIRouter, HTTPException, Form, UploadFile, File, Depends
from datetime import datetime
from database import get_db
from modals import User
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import or_
import schemas
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
            workers = db.query(User).filter(
                or_(
                    User.name.ilike(f"%{name}%"),
                    User.email.ilike(f"%{name}%"),
                    User.city.ilike(f"%{name}%")
                )
            ).all()
        else:
            # If no search term provided, return all workers
            workers = db.query(User).all()
        
        # Convert workers to dictionary format
        worker_list = []
        for worker in workers:
            worker_dict = {
                "id": worker.id,
                "name": worker.name,
                "email": worker.email,
                "phone": worker.phone,
                "address": worker.address,
                "city": worker.city,
                "gender": worker.gender,
                "dob": worker.dob,
                "service": worker.service,
                "experience": worker.exp,
                "availability": worker.availability,
                "id_proof": worker.id_proof,
                "id_proof_number": worker.id_proof_number,
                "about": worker.about,
                "photo_path": worker.photo_path,
                "created_at": worker.created_at.isoformat() if worker.created_at else None,
                "status" : worker.status,
                "religion" : worker.religion
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
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(..., description="Phone number can include country code and special characters (e.g. +91-9999999999)"),
    address: str = Form(...),
    city: str = Form(...),
    gender: str = Form(...),
    dob: str = Form(...),
    service: str = Form(...),
    exp: int = Form(...),
    availability: str = Form(...),
    id_proof: str = Form(...),
    id_proof_number: str = Form(...),
    about: str = Form(...),
    photo: UploadFile = File(...),
    id_document: UploadFile = File(...),
    status : str = "Pending",
    religion : str = "God knows"
):
    try:
        # Generate unique filenames
        photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo.filename}"
        doc_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{id_document.filename}"
        
        # Save files
        photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        doc_path = os.path.join(DOCS_DIR, doc_filename)
        
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
        
        with open(doc_path, "wb") as buffer:
            shutil.copyfileobj(id_document.file, buffer)
        
        # Create database session
        db = next(get_db())
        
        try:
            # Create new worker record
            worker = User(
                name=name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                gender=gender,
                dob=dob,
                service=service,
                exp=exp,
                availability=availability,
                id_proof=id_proof,
                id_proof_number=id_proof_number,
                about=about,
                photo_path=photo_path,
                file_path=doc_path,
                status = status,
                religion = religion,
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
            if os.path.exists(doc_path):
                os.remove(doc_path)
            raise HTTPException(status_code=500, detail=str(e))
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get('/all')
async def get_user(db : Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.delete('/delete-worker/{id}')
async def delete_worker(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"No user found with ID {id}")
    
    db.delete(user)
    db.commit()
    return {"message": f"Deleted user with ID {id}"}

