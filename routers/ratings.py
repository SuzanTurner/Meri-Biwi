from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.workers import Ratings, Worker
from schema import ratings

router = APIRouter(
    prefix = '/ratings',
    tags = "ratings"
)

@router.post('/')
async def post_rating(request : ratings.Ratings, db : Depends = Session (get_db)):
    worker = db.query(Worker).filter(Worker.id == request.id).first()
    if worker:
        rate = Ratings(
            id = request.id,
            user_id = request.user_id,
            rating = request.rating,
            review = request.review
        )

        db.add(rate)
        db.commit()
        db.refresh(rate)

        return {"status" : "success", "messgae" : "Worker rating added!"}
    return {"status" : "failed" , "message" : "Worker id does not exist"}