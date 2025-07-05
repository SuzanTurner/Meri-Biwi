from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from modals.notifications import Notifications
from schema import notifications
import os
import dotenv
import requests

dotenv.load_dotenv()
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")

router = APIRouter(
    tags = ["Notifications"],
    prefix = '/notifications'
)

# @router.post('/')
# async def create_notification(request : notifications.Notifications, db : Session = Depends(get_db)):
#     notification = Notifications(
#         title = request.title,
#         msg = request.msg,
#         msg_type = request.msg_type
#     )
#     db.add(notification)
#     db.commit()
#     db.refresh(notification)

#     return {
#         "status": "success",
#         "message": "Notification created successfully"
#         }

# @router.get('/')
# async def all_notfications(db : Session = Depends(get_db)):
#     all = db.query(Notifications).all()
#     return all


# @router.post("/all")
# def notify_all_users(title: str, message: str):
#     url = "https://onesignal.com/api/v1/notifications"
#     headers = {
#         "Authorization": f"Basic {ONESIGNAL_API_KEY}",
#         "Content-Type": "application/json"
#         }
#     payload = {
#         "app_id": ONESIGNAL_APP_ID,
#         "included_segments": ["All"],
#         "headings": {"en": title},
#         "contents": {"en": message}
#         }
#     response = requests.post(url, json=payload, headers=headers)
#     if response.status_code != 200:
#         raise HTTPException(status_code=500, detail=response.text)
#     return {"status": "success", "response": response.json()}


@router.post("/all")
async def broadcast_notification(request : notifications.Notifications, db : Session = Depends(get_db)):
    notification = Notifications(title=request.title, msg=request.msg, msg_type= request.msg_type)
    db.add(notification)
    db.commit()
    db.refresh(notification)

    # Send via OneSignal
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Authorization": f"Basic {ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "included_segments": ["All"],
        "headings": {"en": request.title},
        "contents": {"en": request.msg}
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)

    return {
        "status": "success",
        "message": "Notification sent and stored successfully",
        "notification_id": notification.id,
        "onesignal_response": response.json()
    }



@router.post("/user")
def notify_user(player_id: str, title: str, message: str):
    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Authorization": f"Basic {ONESIGNAL_API_KEY}",
        "Content-Type": "application/json"
        }
    payload = {
        "app_id": ONESIGNAL_APP_ID,
        "include_player_ids": [player_id],
        "headings": {"en": title},
        "contents": {"en": message}
        }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)
    return {"status": "success", "response": response.json()}

@router.get('/')
async def get_notifications(db: Session = Depends(get_db)):
    notifications_list = db.query(Notifications).all()
    results = [{"id": n.id, "title": n.title, "msg": n.msg, "msg_type": n.msg_type} for n in notifications_list]
    return {"notifications": results}


@router.delete('/')
async def delete_notification(id : int, db : Session = Depends(get_db)):
    notif = db.query(Notifications).filter(Notifications.id == id).first()
    if notif:
        db.delete(notif)
        db.commit()
        return {"status" : "Success", "message" : "Notficaion succesfully deleted"}
    else:
        return {"status" : "failed", "message" : "Notifcation does not exist"}