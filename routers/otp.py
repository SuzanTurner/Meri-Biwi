from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from modals import User
from database import get_db
from datetime import datetime, timedelta
import random

def otp():
    return str(random.randint(100000, 999999))

router = APIRouter(
    tags = ["OTP"],
    prefix = '/otp'
)

@router.post('/send-otp/')
async def send_otp(phone: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if user:
        otp_value = otp()
        user.otp = otp_value
        db.commit()
        return {
            "status": "success",
            "message": "OTP sent successfully!",
            "otp": otp_value  
        }
    else:
        return {
            "status": "no success",
            "message": "OTP not sent, make sure number is registered"
        }


@router.post('/verify-otp/')
async def verify_otp(phone: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == phone).first()
    if not user:
        return {"status": "error", "message": "User not found"}

    print(otp, user.otp)
    print("Now: ", datetime.utcnow())
    print("OTP Created At: ", user.otp_created_at)
    print("Difference: ", datetime.utcnow() - user.otp_created_at)

    if str(user.otp) == otp:
        if datetime.utcnow() - user.otp_created_at > timedelta(minutes=15):
            return {"status": "error", "message": "OTP expired"}
        user.otp = None 
        user.otp_verified = True
        db.commit()
        return {"status": "success", "message": "OTP verified successfully!"}
    else:
        return {"status": "error", "message": "Invalid OTP"}
