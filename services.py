from models import Meals, AdditionalService, Cleaning, AdditionalCleaningPlan
from sqlalchemy.orm import Session
from fastapi import HTTPException
import logging

def get_meals(db: Session):
    try:
        return db.query(Meals).all()
    except Exception as e:
        logging.error(f"Error fetching meals: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_services(db: Session):
    try:
        return db.query(AdditionalService).all()
    except Exception as e:
        logging.error(f"Error fetching services: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
    
def get_cleaning_plans(db: Session):
    try:
        return db.query(Cleaning).all()
    except Exception as e:
        logging.error(f"Error fetching cleaning plans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
def get_additional_cleaning_plans(db: Session):
    try:
        return db.query(AdditionalCleaningPlan).all()
    except Exception as e:
        logging.error(f"Error fetching additional cleaning plans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
