from fastapi import APIRouter, Depends, HTTPException,UploadFile, File,Form,Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional


import os
from modals.services import Service, AdditionalFeature,PlanTypeEnum,FoodTypeEnum
from schemas import (
    ServicePriceOut,
    ServiceOut,
    CategoryEnum,
    AdditionalFeatureCreate,
    AdditionalFeatureOut,
    ServiceUpdate,
)
from database import get_db

router = APIRouter(prefix="/services", tags=["Services"])

UPLOAD_DIR = "/app/data/uploads-service"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")
URL = os.getenv("URL")

os.makedirs(PHOTOS_DIR, exist_ok=True)

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
    service_image_path = os.path.join(PHOTOS_DIR, image.filename)
        
    image_data=image.file.read()
    with open(service_image_path, "wb") as f:
        f.write(image_data)
    # image_base64 = base64.b64encode(image_data).decode("utf-8")
    public_url = f"/uploads-testimonials/photos/{image.filename}"
    full_url = URL + public_url
    cleaned_details = []
    print(service_image_path)
    for item in basic_details:
        parts = item.split(",")  # Split "1 Meal,Dinner"
        cleaned_details.extend([p.strip().lower() for p in parts])
    new_service = Service(
        name=name,
        category=category,
        plan_type=plan_type,
        frequency=frequency,
        number_of=number_of,
        basic_price=basic_price,
        basic_details=cleaned_details,
        duration=duration,
        food_type=food_type,
        is_popular=is_popular,
        description=description,
        image=full_url,
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
@router.get("/filter_services", response_model=ServicePriceOut)
def filter_services(
    plan_type: Optional[PlanTypeEnum] = Query(None),
    food_type: Optional[FoodTypeEnum] = Query(None),
    category: Optional[CategoryEnum] = Query(None),
    frequency: Optional[int] = Query(None),
    number_of: Optional[int] = Query(None),
    meals_per_day:list[str]=Query(None),
    add_service:list[int]=Query(None),
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
    if meals_per_day:
        for meal in meals_per_day:
            meal=meal.strip().lower()
            filters.append(Service.basic_details.any(meal)) 
        
    service = db.query(Service).filter(and_(*filters)).first()
    if not service:
        raise HTTPException(status_code=404, detail="No matching service found")
    additional_services = []
    additional_price=0
    if add_service:
        additional_services = db.query(AdditionalFeature).filter(
            AdditionalFeature.id.in_(add_service)
        ).all()
        additional_price = sum([a.price for a in additional_services])

    total_price = service.basic_price + additional_price

    return {
        "id": service.id,
        "name": service.name,
        "category": service.category,
        "plan_type": service.plan_type,
        "number_of": service.number_of,
        "basic_details": service.basic_details,
        "description": service.description,
        "frequency": service.frequency,
        "duration": service.duration,
        "is_popular": service.is_popular,
        "basic_price": service.basic_price,
        "image": service.image,
        "food_type": service.food_type,
        "additional_service": additional_services,
        "service_price": service.basic_price,
        "additional_service_price": additional_price,
        "total_price": total_price,
    }



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




