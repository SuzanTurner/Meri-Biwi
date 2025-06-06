from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from modals import Service
from schemas import ServiceCreate, ServiceOut, CategoryEnum
from database import get_db

router = APIRouter(prefix="/services", tags=["Services"])


@router.post("/", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.get("/", response_model=List[ServiceOut])
def get_all_services(
    db: Session = Depends(get_db),
    category: Optional[CategoryEnum] = None,
    is_popular: Optional[bool] = None,
):
    query = db.query(Service)
    if category:
        query = query.filter(Service.category == category)
    # if is_popular is not None:
        # query = query.filter(Service.is_popular == is_popular)
    return query.all()


@router.get("/{service_id}", response_model=ServiceOut)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int, updated: ServiceCreate, db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    for field, value in updated.dict().items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)
    return service