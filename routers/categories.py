from fastapi import APIRouter, Depends, UploadFile, Form, File
from database import get_db
from sqlalchemy.orm import Session
from modals.pics import Categories
from datetime import datetime
from urllib.parse import quote
import shutil
import os
import logging
import dotenv
import re

logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads-categories"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")

os.makedirs(PHOTOS_DIR, exist_ok=True)

dotenv.load_dotenv()
BASE_URL = os.getenv('BASE_URL')

router = APIRouter(
    tags = ["Categories"],
    prefix = '/categories'
)

@router.post('/')
async def create_category(
    service_id: str = Form(...),
    image: UploadFile = File(...),
    title: str = Form(...),
    categories : str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        
        safe_orig = re.sub(r'\s+', '_', image.filename)
        photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        photo_path = os.path.join(PHOTOS_DIR, photo_filename)
        
        logger.info(f"Saving image to: {photo_path}")
        
        with open(photo_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
            
        photo_filename = quote(photo_filename)
        public_url = f"/uploads-categories/photos/{photo_filename}"
        # full_url = "http://127.0.0.1:8000" + public_url
        full_url = BASE_URL + public_url
        logger.info(f"Image saved successfully. Public URL: {public_url}")
            
        category = Categories(service_id=service_id, image=full_url, categories = categories, title=title)
        db.add(category)
        db.commit()
        db.refresh(category)
        return {"message": f"Category {category.id} added!", "Category": category}
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        raise

@router.get('/')
async def get_all_categories(db: Session = Depends(get_db)):
    print("HIT: /categories") 
    categories = db.query(Categories).all()
    return categories
    
