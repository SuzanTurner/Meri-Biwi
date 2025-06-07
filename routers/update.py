from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from modals import User
from database import get_db

router = APIRouter(
    tags = ["Update Worker Status"]
)

@router.put("/update/{user_id}")
async def update_user_status(user_id: int, new_status: str, new_religion : str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.status = new_status
    user.religion = new_religion
    db.commit()
    db.refresh(user)
    return {"msg": "Status updated", "user_id": user.id, "username" : user.name, "new_status": user.status, "new_religion" : user.religion}
