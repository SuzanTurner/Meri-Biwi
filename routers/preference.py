from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.workers import Worker
from sqlalchemy import and_

router = APIRouter(
    tags = ["Preference"],
    prefix = '/preferences'
)

@router.get('/')
async def get_worker(date : str,
                   time : str,
                   gender: str,
                   community: str,
                   db : Session = Depends(get_db)):
    workers = db.query(Worker).filter(and_(
                                        Worker.gender == gender,
                                        Worker.religion == community)).all()
    return {
    "data": [
        {"id": worker.id, 
         "name": worker.full_name, 
         "profile_image" : worker.profile_photo_url, 
         "rating" : "5 stars",
         "experience" : worker.experience_years,
         "bio" : "bro is the best (trust me bro)",
         "languages" : worker.languages_spoken,
         "comminity" : worker.religion,
         "gender" : worker.gender}
        for worker in workers
    ]
}
