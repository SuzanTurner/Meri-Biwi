from fastapi import APIRouter, Depends, File, UploadFile, Form
from database import get_db
from sqlalchemy.orm import Session
from modals import Banner
from datetime import datetime
import os
import dotenv
import shutil
import re


dotenv.load_dotenv()
BASE_URL = os.getenv('BASE_URL')

router = APIRouter(
    tags = ['banners'],
    prefix = '/banners'
)

@router.get('/')
async def get_banners(db : Session = Depends(get_db)):
    banners =  db.query(Banner).all()
    return banners

UPLOAD_DIR = "uploads-banners"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")

os.makedirs(PHOTOS_DIR, exist_ok=True)

@router.post('/')
async def create_banners(image : UploadFile = File(...),
                         key : str = Form(...),
                         url : str = Form(...),
                         db : Session = Depends(get_db)):
    
    safe_orig = re.sub(r'\s+', '_', image.filename)
    image_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
    image_path = os.path.join(PHOTOS_DIR, image_filename)
    
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    public_url = f"/uploads-banners/photos/{image_filename}"
    full_url = BASE_URL + public_url
    # full_url = "http://127.0.0.1:8000" + public_url
    
    banner = Banner(
        image = full_url,
        key = key,
        url = url
    )
    
    db.add(banner)
    db.commit()
    db.refresh(banner)
    
    return {"status" : "success", "id" : banner.id, "message" : "banner saved"}