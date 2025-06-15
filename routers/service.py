from fastapi import APIRouter, Depends, HTTPException,UploadFile, File,Form,Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from pathlib import Path

import os

from modals import Service, AdditionalFeature,PlanTypeEnum,FoodTypeEnum
from schemas import (
    ServiceCreate,
    ServiceOut,
    CategoryEnum,
    AdditionalFeatureCreate,
    AdditionalFeatureOut,
    ServiceUpdate,
)
from database import get_db

router = APIRouter(prefix="/services", tags=["Services"])

UPLOAD_DIR = Path("uploads-categories")
SERVICE_PHOTOS_DIR = UPLOAD_DIR / "photos"
SERVICE_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/", response_model=ServiceOut)
def create_service(
    name: str = Form(...),
    category: CategoryEnum = Form(...),
    plan_type: PlanTypeEnum = Form(...),
    frequency: int = Form(...),
    number_of: int = Form(...),
    basic_price: float = Form(...),
    basic_details: list[str] = Form(...),  # Will need to send this as comma-separated
    duration: float = Form(...),
    food_type: Optional[FoodTypeEnum] = Form(None),
    is_popular: bool = Form(False),
    description: Optional[str] = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Store the image or get its path
    service_image_path = os.path.join(SERVICE_PHOTOS_DIR, image.filename)
        
    with open(service_image_path, "wb") as f:
        f.write(image.file.read())
        
    new_service = Service(
        name=name,
        category=category,
        plan_type=plan_type,
        frequency=frequency,
        number_of=number_of,
        basic_price=basic_price,
        basic_details=basic_details,
        duration=duration,
        food_type=food_type,
        is_popular=is_popular,
        description=description,
        image=service_image_path,  # Save path to DB
    )
    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service


@router.get("/", response_model=List[ServiceOut])
def get_all_services(
    db: Session = Depends(get_db),
    category: Optional[CategoryEnum] = None,
):
    query = db.query(Service)
    if category:
        query = query.filter(Service.category == category)


    services = query.all()
    return services
@router.get("/filter_services", response_model=List[ServiceOut])
def filter_services(
    plan_type: Optional[PlanTypeEnum] = Query(None),
    food_type: Optional[FoodTypeEnum] = Query(None),
    category: Optional[CategoryEnum] = Query(None),
    frequency: Optional[int] = Query(None),
    number_of: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    filters = []

    if plan_type:
        filters.append(Service.plan_type == plan_type)
    if category:
        filters.append(Service.category == category)
    if frequency:
        filters.append(Service.frequency == frequency)
    if number_of:
        filters.append(Service.number_of == number_of)
    if food_type:
        filters.append(Service.food_type == food_type)

    results = db.query(Service).filter(and_(*filters)).all()
    print(results)
    return results



@router.get("/{service_id}", response_model=ServiceOut)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return service


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int, updated: ServiceUpdate, db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = updated.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)
    return service



@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return {"detail": "Service deleted successfully"}


@router.post("/features/", response_model=AdditionalFeatureOut)
def add_additional_feature(
    feature: AdditionalFeatureCreate, db: Session = Depends(get_db)
):
    db_feature = AdditionalFeature(**feature.dict())
    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature

@router.delete("/features/{feature_id}")
def delete_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = (
        db.query(AdditionalFeature).filter(AdditionalFeature.id == feature_id).first()
    )
    if not feature:
        raise HTTPException(status_code=404, detail="AdditionalFeature not found")
    db.delete(feature)
    db.commit()
    return {"detail": "feature deleted successfully"}

@router.get("/features/", response_model=List[AdditionalFeatureOut])
def get_all_additional_feature(
    db: Session = Depends(get_db)
):
    query=db.query(AdditionalFeature)
    return query.all()




