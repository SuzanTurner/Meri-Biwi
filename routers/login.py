
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modals import User, Admin
from schemas import UserLogin, AdminLogin
from database import get_db
from hashing import Hash

router = APIRouter(
    tags = ["User Login"],
    prefix = '/login'
)

@router.post('/user')
def user_login(request : UserLogin, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail= "User with this email is not found")
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Invalid Password")
    
    return {"message": " USER Logged in successfully", "email": user.email}

@router.post('/admin')
def admin_login(request : AdminLogin, db : Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == request.email).first()
    
    if not admin:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail= "Admin with this email is not found")
    
    if not Hash.verify(request.password, admin.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Invalid Password")
    
    return {"message": " ADMIN Logged in successfully", "email": admin.email}
    
        