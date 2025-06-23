from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from hashing import Hash
from modals.admin import Admin
from routers.categories import BASE_URL
from schemas import UpdateAdmin
from datetime import datetime
from database import get_db
from urllib.parse import quote
import bcrypt
import shutil
import pytz
import os
import re
import dotenv


dotenv.load_dotenv()
BASE_URL = os.getenv('BASE_URL')

router = APIRouter(
    tags = ["Admin"],
    prefix = '/admin'
)

UPLOAD_DIR = "/app/data/uploads-admin"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")

os.makedirs(PHOTOS_DIR, exist_ok=True)


@router.post('/')
async def create_admin(
    username : str = Form(...),
    email : str = Form(...),
    password : str = Form(...),
    full_name : str = Form(...),
    profile_image : UploadFile = File(...),
    role : str = Form(...),
    status : bool = False,
    db : Session = Depends (get_db)):
    
    all_admins = db.query(Admin).all()
    for admin in all_admins:
        if bcrypt.checkpw(password.encode('utf-8'), admin.password.encode('utf-8')):
            raise HTTPException(
                status_code=400,
                detail="This password is already used by another admin"
            )
            
    safe_orig = re.sub(r'\s+', '_', profile_image.filename)
    photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
            
    # photo_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{profile_image.filename}"
    photo_path = os.path.join(PHOTOS_DIR, photo_filename)
    
    with open(photo_path, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)
        
        
    photo_filename = quote(photo_filename)
    public_url = f"/uploads-admin/photos/{photo_filename}"
    full_url = BASE_URL + public_url
    # full_url = "http://127.0.0.1:8000" + public_url

    
    hashed_password = Hash.bcrypt(password) 
    admin = Admin(
        username = username,
        email = email,
        password = hashed_password,
        full_name = full_name,
        profile_image = full_url,
        role = role,
        status = status,
    )
    
    db.add (admin)
    db.commit()
    db.refresh(admin)
    
    return {
        "status": "success",
        "message": "Worker registration successful",
        "user_id": admin.id,
        "username" : admin.username
    }

@router.get('/')
async def get_admin(db : Session = Depends(get_db)):
    admins = db.query(Admin).all()
    return admins

@router.get('/{id}')
async def get_admin_by_ID(id : int, db : Session = Depends(get_db)):
    user = db.query(Admin).filter(Admin.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail= f"User with id {id} does not exist")
    return user

@router.delete('/{id}')
async def delete_user(id : int, db : Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
    db.delete(admin)
    db.commit()
    return {"message" : "Admin Deleted"}


@router.put("/{id}")
def update_user_status(id: int,
                       update_data: UpdateAdmin,
                       db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = {
        key: value for key, value in update_data.dict(exclude_unset=True).items()
        if value not in ["string", "", None]
    }

    # Update fields except password first
    for key, value in update_dict.items():
        if key != "password":
            setattr(admin, key, value)

    # Handle password update & hashing if password provided
    if "password" in update_dict:
        hashed_password = Hash.bcrypt(update_dict["password"])
        admin.password = hashed_password

    # Update timestamp
    ist = pytz.timezone("Asia/Kolkata")
    admin.updated_at = datetime.now(ist)

    db.commit()
    db.refresh(admin)

    return {"msg": "User updated successfully", "user_details": admin}