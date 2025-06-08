from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter(
    tags = ["Check Database"]
)

# @router.get("/db-check")
# def get_current_db(db: Session = Depends(get_db)):
#     result = db.execute(text("SELECT current_database();"))
#     return {"connected_database": list(result)[0][0]}

@router.get("/db-check")
def get_current_db(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT DATABASE();"))
    return {"connected_database": list(result)[0][0]}