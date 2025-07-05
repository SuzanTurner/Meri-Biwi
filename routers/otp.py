from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from modals.otp import Otp
from modals.users import User
from database import get_db
import random
import requests
import dotenv
import os

dotenv.load_dotenv()
API_KEY = os.getenv("OTP_API_KEY")


def generate_otp():
    return random.randint(1000, 9999)

router = APIRouter(
    tags = ["OTP"],
    prefix = '/otp'
)


@router.post("/send-otp/")
async def send_otp(phone: str, db: Session = Depends(get_db)):
    otp_value = generate_otp()
    
    MOBILE = phone
    OTP = otp_value

    url = f"https://apihome.in/panel/api/bulksms/?key={API_KEY}&mobile={MOBILE}&otp={OTP}"

    response = requests.get(url)

    print(response.text)
    
    db.query(Otp).filter(Otp.phone == phone).delete()
    
    new_otp = Otp(phone=phone, otp=otp_value)
    db.add(new_otp)
    db.commit()
    return {
        "status": "success",
        "message": "OTP sent successfully!",
        "otp": otp_value,
        "data" : response.text,
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
