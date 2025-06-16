from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from schemas import Testimonials as TestSchema
from modals import Testimonials
import shutil
import os
import dotenv
import re

dotenv.load_dotenv()
BASE_URL = os.getenv('BASE_URL')


router = APIRouter(
    tags = ["Testimonials"],
    prefix = '/testimonials'
)


UPLOAD_DIR = "uploads-testimonials"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos/videos")

os.makedirs(PHOTOS_DIR, exist_ok=True)

@router.post('/')
async def create_testimonial(image_or_video : UploadFile = File(...),
                             title: str = Form(...),
                             description : str = Form(...),
                             db: Session = Depends(get_db)):
    
    
    safe_orig = re.sub(r'\s+', '_', image_or_video.filename)
    photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
    photo_path = os.path.join(PHOTOS_DIR, photo_filename)
    
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(image_or_video.file, buffer)
        
    public_url = f"/uploads-testimonials/photos/{photo_filename}"
    full_url = BASE_URL + public_url
    # full_url = "http://127.0.0.1:8000" + public_url
    
    datatype = image_or_video.content_type
    
    testimony = Testimonials(image_or_video=full_url, datatype = datatype, title=title, description = description)
    db.add(testimony)
    db.commit()
    db.refresh(testimony)
    
    return {"status" : "success", "message" : f"Testimony with id {testimony.id} succesfully created!"}

@router.get('/')
async def get_testimonials(db : Session = Depends(get_db)):
    testimonies = db.query(Testimonials).all()
    return testimonies


@router.put("/{id}", response_model=TestSchema)
def update_testimonial(
    id: int, updated: TestSchema, db: Session = Depends(get_db)
):
    testimonial = db.query(Testimonials).filter(Testimonials.id == id).first()
    if not testimonial:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = updated.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(testimonial, field, value)

    db.commit()
    db.refresh(testimonial)
    return testimonial

@router.delete('/{id}')
async def delete_testimonial(id : int, db : Session = Depends(get_db)):
    feature = (
        db.query(Testimonials).filter(Testimonials.id == id).first()
    )
    if not feature:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    db.delete(feature)
    db.commit()
    return {"status":"success", "detail": "feature deleted successfully"}
