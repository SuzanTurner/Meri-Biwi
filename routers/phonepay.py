import json
import base64
import hashlib
import httpx
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import get_db
from modals.phonepay import Phonepay
from schema import phonepay
import uuid
import os
import dotenv

dotenv.load_dotenv()
MERCHANT_ID = os.getenv("MERCHANT_ID")
SALT_KEY = os.getenv("SALT_KEY")
SALT_INDEX = os.getenv("SALT_INDEX")
BASE_URL = os.getenv("BASE_URL")
REDIRECT_URL = os.getenv("REDIRECT_URL")
CALLBACK_URL = os.getenv("CALLBACK_URL")


router = APIRouter(
    tags = ['Phonepay Integration'],
    prefix = '/phonepay'
)

def generate_transaction_id():
    return str(uuid.uuid4())

@router.post("/phonepe/initiate")
async def initiate_transaction(amount: int, user_id: int,  db : Session = Depends(get_db)):
    merchant_transaction_id = generate_transaction_id()
    payload = {
        "merchantId": MERCHANT_ID,
        "merchantTransactionId": merchant_transaction_id,
        "merchantUserId": str(user_id),
        "amount": amount,
        "redirectUrl": REDIRECT_URL,
        "redirectMode": "POST",
        "callbackUrl": CALLBACK_URL,
        "paymentInstrument": {
            "type": "PAY_PAGE"
            }
        }
    payload_json = json.dumps(payload, separators=(',', ':'))
    base64_payload = base64.b64encode(payload_json.encode()).decode()
    string_to_hash = f"{base64_payload}/pg/v1/pay{SALT_KEY}"
    x_verify = hashlib.sha256(string_to_hash.encode()).hexdigest() + "###" + SALT_INDEX

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/pg/v1/pay",
            headers={
            "Content-Type": "application/json",
            "X-VERIFY": x_verify,
            "X-MERCHANT-ID": MERCHANT_ID
            },
            json={"request": base64_payload}
            )
        
    res_data = response.json()

    if res_data["success"]:

        phonepay = Phonepay(
            merchant_transaction_id = merchant_transaction_id,
            amount  = amount,
            status = "Success",
            user_id = user_id,
        )
        db.add(phonepay)
        db.commit()
        db.refresh(phonepay)

        return {
            "status": "Success",
            "redirect_url": res_data["data"]["instrumentResponse"]
            ["redirectInfo"]["url"]
            }
    
    else:
        raise HTTPException(status_code=400, detail="Payment initiation failed")


@router.post("/phonepe/callback")
async def payment_callback(request : phonepay.Phonepay,  db : Session = Depends(get_db)):
    phonepay = db.query(Phonepay).filter(and_(Phonepay.merchant_transaction_id == request.merchant_transaction_id,
                                              Phonepay.id == id)).first()
    
    Phonepay.status = request.status
    if not phonepay:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.commit()
    db.refresh(phonepay)
    return {"status": "success"}