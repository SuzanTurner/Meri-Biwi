from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.workers import Ratings, Worker
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


# @router.get('/{worker_id}')
# async def get_rating(worker_id: int, db: Session = Depends(get_db)):
#     rating = db.query(Ratings).filter(
#         Ratings.worker_id == worker_id,
#     ).all()

#     if not rating:
#         return {"status": "error", "message": "Rating not found"}

#     total = sum(r.rating for r in rating)
#     count = len(rating)
#     avg_rating = round(total / count, 2)

#     worker = db.query(Worker).filter(Worker.id == worker_id).first()

#     if not worker:
#         return {"status": "error", "message": "Worker not found"}
#     worker.rating = avg_rating
#     db.commit()
#     db.refresh(worker)

#     return {"status": "success", 
#             # "rating" : avg_rating,
#              "data": rating}

@router.get("/{worker_id}")
async def get_rating(worker_id: int, db: Session = Depends(get_db)):
    rating = db.query(Ratings).filter(Ratings.worker_id == worker_id).all()
    if not rating:
        return {"status": "error", "message": "Rating not found"}

    total = sum(r.rating for r in rating)
    count = len(rating)
    avg_rating = round(total / count, 2)

    worker = db.query(Worker).filter(Worker.id == worker_id).first()

    if not worker:
        return {"status": "error", "message": "Worker not found"}
    worker.rating = avg_rating
    db.commit()
    db.refresh(worker)

    return {"status": "success", 
            "rating" : avg_rating,
             "data": [ratings.RatingsResponse.model_validate(r) for r in rating]}