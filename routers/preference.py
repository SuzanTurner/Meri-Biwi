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
                   service_type : str,
                   community: str,
                   db : Session = Depends(get_db)):
    
    if community.lower() == "any":
        workers = db.query(Worker).filter(Worker.gender == gender).all()
        return {
            "data": [
                {"id": worker.id, 
                "name": worker.full_name, 
                "profile_image" : worker.profile_photo_url, 
                "rating" : "5",
                "experience" : worker.experience_years,
                "bio" : worker.bio,
                "languages" : worker.languages_spoken,
                "community" : worker.religion,
                "gender" : worker.gender}
                for worker in workers
            ]
                }
        
    workers = db.query(Worker).filter(and_(
                                        Worker.gender == gender,
                                        Worker.religion == community)).all()
    return {
    "data": [
        {"id": worker.id, 
         "name": worker.full_name, 
         "profile_image" : worker.profile_photo_url, 
         "rating" : "5",
         "experience" : worker.experience_years,
         "bio" : worker.bio,
         "languages" : worker.languages_spoken,
         "community" : worker.religion,
         "gender" : worker.gender}
        for worker in workers
    ]
}



# @router.get("/")
# async def get_worker(
#     date: str ,  # required
#     time: str,  # required
#     gender: str,  # required
#     community: str ,  # default to 'any'
#     db: Session = Depends(get_db)
# ):
#     try:
#         # basic filter
#         query = db.query(Worker).filter(Worker.gender == gender)

#         # add community filter only if not 'any'
#         if community.lower() != "any":
#             query = query.filter(Worker.religion == community)

#         workers = query.all()

#         return {
#             "data": [
#                 {
#                     "id": worker.id,
#                     "name": worker.full_name,
#                     "profile_image": worker.profile_photo_url,
#                     "rating": "5",  # static for now
#                     "experience": worker.experience_years,
#                     "bio": worker.bio,
#                     "languages": worker.languages_spoken,
#                     "community": worker.religion,
#                     "gender": worker.gender
#                 }
#                 for worker in workers
#             ]
#         }
#     except Exception as e:
#         return {"status": "error", "message": str(e)}