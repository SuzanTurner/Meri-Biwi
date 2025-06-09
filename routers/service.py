from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from modals import Service, AdditionalFeature
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


@router.post("/", response_model=ServiceOut)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    features = []
    if service.additional_feature_ids:
        features = (
            db.query(AdditionalFeature)
            .filter(AdditionalFeature.id.in_(service.additional_feature_ids))
            .all()
        )
        if len(features) != len(service.additional_feature_ids):
            raise HTTPException(
                status_code=400, detail="One or more additional features do not exist"
            )

    db_service = Service(
        **service.dict(exclude={"additional_feature_ids"}), additional_features=features
    )
    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return {
        **db_service.__dict__,
        "additional_feature_ids": [f.id for f in db_service.additional_features],
    }


@router.get("/", response_model=List[ServiceOut])
def get_all_services(
    db: Session = Depends(get_db),
    category: Optional[CategoryEnum] = None,
    is_popular: Optional[bool] = None,
):
    query = db.query(Service)
    if category:
        query = query.filter(Service.category == category)


    services = query.all()
    return [
        {
            **service.__dict__,
            "additional_feature_ids": [f.id for f in service.additional_features],
        }
        for service in services
    ]


@router.get("/{service_id}", response_model=ServiceOut)
def get_service_by_id(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    return {
        **service.__dict__,
        "additional_feature_ids": [f.id for f in service.additional_features],
    }


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int, updated: ServiceUpdate, db: Session = Depends(get_db)
):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    update_data = updated.dict(exclude_unset=True)

    if "additional_feature_ids" in update_data:
        features = (
            db.query(AdditionalFeature)
            .filter(AdditionalFeature.id.in_(update_data.pop("additional_feature_ids")))
            .all()
        )
        if len(features) != len(update_data["additional_feature_ids"]):
            raise HTTPException(
                status_code=400, detail="One or more additional features do not exist"
            )
        service.additional_features = features
        update_data.pop("additional_feature_ids")

        service.additional_features = features

    for field, value in update_data.items():
        setattr(service, field, value)

    db.commit()
    db.refresh(service)

    return {
        **service.__dict__,
        "additional_feature_ids": [f.id for f in service.additional_features],
    }


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

@router.get("/features/", response_model=List[AdditionalFeatureOut])
def get_all_additional_feature(
    db: Session = Depends(get_db)
):
    query=db.query(AdditionalFeature)
    return query.all()




