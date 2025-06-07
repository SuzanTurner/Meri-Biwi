from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import UserUpdate
from modals import User
from database import get_db

router = APIRouter(
    tags = ["Update Worker Status"]
)

# @router.put("/update/{user_id}")
# async def update_user_status(user_id: int, 
#                              new_status: str, 
#                              new_religion : str,
#                              new_phone : str,
#                              new_email : str,
#                              new_address : str,
#                              new_service : str,
#                              new_availabilty : str, 
#                              db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     user.status = new_status
#     user.religion = new_religion
#     user.phone = new_phone
#     user.email = new_email
#     user.address = new_address
#     user.service = new_service
#     user.availability = new_availabilty
#     db.commit()
#     db.refresh(user)
#     return {"msg": "Status updated", "user_details " : user }


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
                             update_data: UserUpdate,
                             db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_dict = {
        key: value for key, value in update_data.dict(exclude_unset=True).items()
        if value not in ["string", "", None]  # 👈 ignore placeholder garbage
    }

    for key, value in update_dict.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return {"msg": "User updated successfully", "user_details": user}

