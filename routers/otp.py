from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from modals.otp import Otp
from modals.users import User
from database import get_db
import random

def generate_otp():
    return random.randint(1000, 9999)

router = APIRouter(
    tags = ["OTP"],
    prefix = '/otp'
)

@router.post("/send-otp/")
async def send_otp(phone: str, db: Session = Depends(get_db)):
    otp_value = generate_otp()
    
    db.query(Otp).filter(Otp.phone == phone).delete()
    
    new_otp = Otp(phone=phone, otp=otp_value)
    db.add(new_otp)
    db.commit()
    return {
        "status": "success",
        "message": "OTP sent successfully!",
        "otp": otp_value  
    }


@router.post("/verify-otp/")
async def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    record = db.query(Otp).filter(Otp.phone == phone, Otp.otp == otp).first()
    if not record:
        return {"status": "error", "message": "Invalid OTP or phone number"}

    if datetime.utcnow() - record.created_at > timedelta(minutes=15):
        return {"status": "error", "message": "OTP expired"}

    user = db.query(User).filter(User.phone == phone).first()
    if user:
        user.otp_verified = True
        db.commit()
    # db.delete(record)
    db.commit()

    return {"status": "success", "message": "OTP verified successfully!"}
