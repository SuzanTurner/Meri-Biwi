
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modals import User
from schemas import UserLogin
from database import get_db
from hashing import Hash

router = APIRouter(
    tags = ["User Login"],
    prefix = '/login'
)

@router.post('/')
def login(request : UserLogin, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    # print(user)
    
    if not user:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail= "User with this email is not found")
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Invalid Password")
    
    return {"message": "Logged in successfully", "email": user.email}
    
        