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
    return workers