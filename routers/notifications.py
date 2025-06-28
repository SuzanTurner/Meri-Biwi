from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.notifications import Notifications
from schema import notifications

router = APIRouter(
    tags = ["Notifications"],
    prefix = '/notifications'
)

@router.post('/')
async def create_notification(request : notifications.Notifications, db : Session = Depends(get_db)):
    notification = Notifications(
        title = request.title,
        msg = request.msg,
        msg_type = request.msg_type
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {
        "status": "success",
        "message": "Notification created successfully"
        }

@router.get('/')
async def all_notfications(db : Session = Depends(get_db)):
    all = db.query(Notifications).all()
    return all