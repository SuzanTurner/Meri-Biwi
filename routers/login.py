from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from . import hashing
import schemas
import modals

router = APIRouter(
    tags = ["Login"]
)

@router.post("/login")
async def login(request : schemas.Login, db : Session = Depends(get_db)):
    user = db.query(modals.User_Login).filter(modals.User_Login.username == request.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= "Invalid Credentials")
    if not hashing.hash.verify(request.password, user.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= "Invalid Password")
        
    return {"message": "Logged in successfully", "username": user.username}