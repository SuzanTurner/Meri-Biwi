
from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import hashing
import schemas
import modals

router = APIRouter(
    tags = ["Users"]
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

@router.post('/user')
async def create_user(request : schemas.User, db : Session = Depends(get_db)):
    # hashed_password = pwd_context.hash(request.password)
    new_user = modals.User_Login(username = request.username, password = hashing.hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message" : "User Created ", "User" : new_user.username}

@router.get('/user/{id}')
async def get_user(id : int, db : Session = Depends(get_db)):
    user = db.query(modals.User_Login).filter(modals.User_Login.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"User with {id} is not found")
    return user.username