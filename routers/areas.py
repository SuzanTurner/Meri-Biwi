from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from modals.areas import Areas
from typing import Optional
import schemas
import math


router = APIRouter(
    tags = ["Areas"],
    prefix = "/areas"
)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in kilometers

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = math.sin(d_lat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(d_lon / 2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # in kilometers

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


@router.get('/pincode')
async def check_areas(pincode : str, 
                      latitude: Optional[float] = None,
                      longitude: Optional[float] = None,
                      db : Session = Depends(get_db)):
    area = db.query(Areas).filter(Areas.pincode == pincode).first()
    if area:
        return {"status" : "success", "area" : area}
    else:
        all_areas = db.query(Areas).all()
        nearby_areas = []

        for a in all_areas:
            if a.latitude is not None and a.longitude is not None:
                dist = haversine(latitude, longitude, a.latitude, a.longitude)
                if dist <= 5:
                    nearby_areas.append({
                        "area_name": a.area_name,
                        "pincode": a.pincode,
                        "latitude": a.latitude,
                        "longitude": a.longitude,
                        "landmark": a.landmark,
                        "distance_km": round(dist, 2)
                    })

        if nearby_areas:
            return {
                "status": "Success",
                "message": "Found nearby areas within 5 km.",
                # "areas found" : len(nearby_areas),
                # "areas": sorted(nearby_areas, key=lambda x: x["distance_km"])
            }
        else:
            return {
                "status": "error",
                "detail": "No nearby serviceable areas found within 5 km radius."
            }

            

