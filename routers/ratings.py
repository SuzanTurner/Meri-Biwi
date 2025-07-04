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
async def post_rating(request : ratings.Ratings, db : Session = Depends(get_db)):
    pass