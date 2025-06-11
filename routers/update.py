from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import WorkerUpdate
from modals import Worker
from database import get_db

router = APIRouter(
    tags = ["Update Worker Status"]
)


# @router.put("/update/{user_id}")
# async def update_user_status(user_id: int,
#                              update_data: UserUpdate,
#                              db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     update_dict = update_data.dict(exclude_unset=True)  # 🧠 This is key

#     for key, value in update_dict.items():
#         setattr(user, key, value)

#     db.commit()
#     db.refresh(user)
#     return {"msg": "User updated successfully", "user_details": user}


@router.put("/update/{user_id}")
async def update_user_status(user_id: int,
                             update_data: WorkerUpdate,
                             db: Session = Depends(get_db)):

    user = db.query(Worker).filter(Worker.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = {
        key: value for key, value in update_data.dict(exclude_unset=True).items()
        if value not in ["string", "", None]  
    }

    for key, value in update_dict.items():
        setattr(user, key, value)
        

    db.commit()
    db.refresh(user)

    return {"msg": "User updated successfully", "user_details": user}

