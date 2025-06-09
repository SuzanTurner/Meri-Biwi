from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from modals import User
from schemas import UpdateUser
from database import get_db
from datetime import datetime
import hashing
import uuid
import pytz


router = APIRouter(
    tags = ["Users"],
    prefix = "/users"
)

@router.get("/")
async def get_users(db : Session = Depends(get_db)):
    users = db.query(User).all()
    return users


def generate_unique_id():
    return uuid.uuid4().hex[:10]

@router.post("/")
async def create_user(
    phone: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    otp_verified: bool = False,
    # fcm_token : str,
    wallet: float = 0.00,
    status: bool = False,
    address_line_1: str = Form(...),
    address_line_2: str = Form(...),
    city: str = Form(...),
    db: Session = Depends(get_db)):

    uid = generate_unique_id()

    while db.query(User).filter(User.uid == uid).first():
        uid = generate_unique_id()

    hashed_password = hashing.Hash.bcrypt(password) 
    user = User(
        uid=uid,
        phone=phone,
        email=email,
        password= hashed_password,
        otp_verified=otp_verified,
        wallet=wallet,
        status=status,
        address_line_1=address_line_1,
        address_line_2=address_line_2,
        city=city,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "message": "Worker registration successful",
        "user_id": user.id,
        "user_uid" : user.uid
    }


# @router.put("/{id}")
# async def update_user_status(id: int,
#                              update_data: UpdateUser,
#                              db: Session = Depends(get_db)):

#     user = db.query(User).filter(User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     update_dict = {
#         key: value for key, value in update_data.dict(exclude_unset=True).items()
#         if value not in ["string", "", None]  
#     }

#     for key, value in update_dict.items():
#         setattr(user, key, value)
        
#     hashed_password = hashing.Hash.bcrypt(UpdateUser.password) 
#     user.password = hashed_password
    
#     ist = pytz.timezone("Asia/Kolkata") 
#     user.updated_at = datetime.now(ist)

#     db.commit()
#     db.refresh(user)

#     return {"msg": "User updated successfully", "user_details": user}

@router.put("/{id}")
def update_user_status(id: int,
                       update_data: UpdateUser,
                       db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = {
        key: value for key, value in update_data.dict(exclude_unset=True).items()
        if value not in ["string", "", None]
    }

    # Update fields except password first
    for key, value in update_dict.items():
        if key != "password":
            setattr(user, key, value)

    # Handle password update & hashing if password provided
    if "password" in update_dict:
        hashed_password = hashing.Hash.bcrypt(update_dict["password"])
        user.password = hashed_password

    # Update timestamp
    ist = pytz.timezone("Asia/Kolkata")
    user.updated_at = datetime.now(ist)

    db.commit()
    db.refresh(user)

    return {"msg": "User updated successfully", "user_details": user}


@router.get('/{id}')
async def get_user_by_id(id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail= f"User with id {id} does not exist")
    return user
    
@router.delete('/{id}')
async def delete_user(id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
    db.delete(user)
    db.commit()
    return {"message" : "User Deleted"}
