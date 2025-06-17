
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modals import User, Admin
from schemas import UserLogin, AdminLogin
from database import get_db
from hashing import Hash

router = APIRouter(
    tags = ["Login"],
    prefix = '/login'
)

@router.post('/user')
def user_login(request : UserLogin, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.phone == request.phone).first()
    
    if not user:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail= "User with this phone is not found")
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Invalid Password")
    
    return {"status": "success", "message": "login successful", "id" : user.id, "phone" : user.phone, "uid" : user.uid, "token":"acbd1234"}

@router.post('/admin')
def admin_login(request : AdminLogin, db : Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.email == request.email).first()
    
    if not admin:
        raise HTTPException( status_code = status.HTTP_404_NOT_FOUND, detail= "Admin with this email is not found")
    
    if not Hash.verify(request.password, admin.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "Invalid Password")
    
    return {"status": "success", "message": "login successful", "token":"acbd1234"}
    
        