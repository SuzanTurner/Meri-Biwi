from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from modals import User
from schemas import UpdateUser,UserCreate
from database import get_db
from datetime import datetime
import hashing
import uuid
import pytz
import bcrypt

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
    UserData:UserCreate,
    db: Session = Depends(get_db)):
    
    try:

        uid = generate_unique_id()

        while db.query(User).filter(User.uid == uid).first():
            uid = generate_unique_id()
        password = UserData.password
        # all_users = db.query(User).all()
        # for user in all_users:
        #     if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        #         raise HTTPException(
        #             status_code=400,
        #             detail="This password is already used by another user",  # 😂😂😂
        #         )
                
        hashed_password = hashing.Hash.bcrypt(password) 
        email = UserData.email if UserData.email.strip() else None

        user = User(
            uid=uid,
            name=UserData.name,
            phone=UserData.phone,
            email=email,
            password=hashed_password,
            otp_verified=False,
            wallet=0.0,
            status=False,
            address_line_1="x",
            address_line_2="x",
            city="x",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "status": "success",
            "message": "User registration successful",
            "user_id": user.id,
            "user_uid" : user.uid
        }
    except Exception as e:
        print("User creation error:", str(e))
        return {"status" : "error", "message" : "Invalid or missing phone number"}

@router.put("/{uid}")
def update_user_(uid: str,
                update_data: UpdateUser,
                db: Session = Depends(get_db)):

    user = db.query(User).filter(User.uid == uid).first()
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

    return {"status": "success", "user_details": user}


@router.get('/{uid}')
async def get_user_by_id(uid : str, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail= f"User with id {uid} does not exist")
    return user
    
    
@router.delete('/{id}')
async def delete_user(id : int, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} does not exist")
    db.delete(user)
    db.commit()
    return {"message" : "User Deleted"}
