from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from datetime import datetime
from schemas import Testimonials as TestSchema
from modals.pics import Testimonials
from urllib.parse import quote
import shutil
import os
import dotenv
import re
import base64

dotenv.load_dotenv()
URL = os.getenv('URL')
# BASE_URL = "http://127.0.0.1:8000"


router = APIRouter(
    tags = ["Testimonials"],
    prefix = '/testimonials'
)


UPLOAD_DIR = "/app/data/uploads-testimonials"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")

os.makedirs(PHOTOS_DIR, exist_ok=True)

@router.post('/')
async def create_testimonial(image_or_video : UploadFile = File(...),
                             title: str = Form(...),
                             categories : str = Form(...),
                             description : str = Form(...),
                             db: Session = Depends(get_db)):
    
    safe_orig = re.sub(r'\s+', '_', image_or_video.filename)
    photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
    photo_path = os.path.join(PHOTOS_DIR, photo_filename)
    
    # image_data = await image_or_video.read()
    
    # with open(photo_path, "wb") as buffer:
    #     shutil.copyfileobj(image_or_video.file, buffer)
        
    # photo_filename = quote(photo_filename)
    # public_url = f"/uploads-testimonials/photos/{photo_filename}"
    # full_url = BASE_URL + public_url
    # full_url = "http://127.0.0.1:8000" + public_url
    
    image_data = await image_or_video.read()

    # ✅ Save to disk using that same data
    with open(photo_path, "wb") as buffer:
        buffer.write(image_data)

    # ✅ Build the URL safely
    photo_filename_enc = quote(photo_filename, safe="")
    public_url = f"/uploads-testimonials/photos/{photo_filename_enc}"
    full_url = URL + public_url
    
    datatype = image_or_video.content_type
    
    testimony = Testimonials(image_or_video=full_url, datatype = datatype,  categories = categories, title=title, description = description)
    db.add(testimony)
    db.commit()
    db.refresh(testimony)
    
    return {"status" : "success", "message" : f"Testimony with id {testimony.id} succesfully created!"}

@router.get('/')
async def get_testimonials(db: Session = Depends(get_db)):
    testimonies = db.query(Testimonials).all()
    results = [{"id": t.id, "title" : t.title ,"datatype" : t.datatype,"categories" : t.categories ,"url": t.image_or_video} for t in testimonies]
    return {"testimonials": results}



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
