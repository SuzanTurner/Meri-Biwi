from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from modals.areas import Areas
import schemas


router = APIRouter(
    tags = ["Areas"],
    prefix = "/areas"
)

@router.post('/')
async def add_area(request : schemas.Areas, db : Session = Depends(get_db)):
    try:
        area = Areas(
            area_name = request.area_name,
            latitude = request.latitude,
            longitude = request.longitude,
            pincode = request.pincode,
            landmark = request.landmark
        )
        db.add(area)
        db.commit()
        db.refresh(area)
        
        return {"status" : "success", "message" : "Area added"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Area not added")
    
@router.get('/')
async def get_areas(db : Session = Depends(get_db)):
    areas = db.query(Areas).all()
    return areas