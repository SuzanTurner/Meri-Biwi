from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.workers import Ratings
from schema import ratings

router = APIRouter(
    tags = ["Ratings"],
    prefix = "/ratings",
)

@router.post('/')
async def post_rating(request : ratings.Ratings, db : Session = Depends(get_db)):
    rating = Ratings(
        worker_id = request.worker_id,
        user_uid = request.user_uid,
        booking_id = request.booking_id,
        rating = request.rating,
        comments = request.comments
    )

    db.add(rating)
    db.commit()
    db.refresh(rating)

    return {"status" : "success", "message": "Rating added successfully", "data": rating}


@router.get('/{worker_id}')
async def get_rating(worker_id: int, db: Session = Depends(get_db)):
    rating = db.query(Ratings).filter(
        Ratings.worker_id == worker_id,
    ).all()

    if not rating:
        return {"status": "error", "message": "Rating not found"}

    return {"status": "success", "data": rating}
