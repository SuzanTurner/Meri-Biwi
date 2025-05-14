from models import V_Breakfast_Lunch
from sqlalchemy.orm import Session
from schemas import Veg_Breakfast_Lunch_Create
import logging
from sqlalchemy import inspect
from fastapi import HTTPException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_veg_breakfast_lunch(db: Session, data: Veg_Breakfast_Lunch_Create ):
    veg_breakfast_lunch_instance = V_Breakfast_Lunch(**data.model_dump())
    db.add(veg_breakfast_lunch_instance)
    db.commit()
    db.refresh(veg_breakfast_lunch_instance)
    return veg_breakfast_lunch_instance

def get_veg_breakfast_lunch(db: Session):
    try:
        logger.info("Attempting to fetch all veg breakfast lunch records")
        
        # Check if table exists
        inspector = inspect(db.get_bind())
        tables = inspector.get_table_names()
        logger.info(f"Available tables: {tables}")
        
        if 'Veg_Breakfast_Lunch' not in tables:
            raise HTTPException(status_code=500, detail="Table 'Veg_Breakfast_Lunch' does not exist")
        
        # Get column information
        columns = inspector.get_columns('Veg_Breakfast_Lunch')
        logger.info(f"Table columns: {[col['name'] for col in columns]}")
        
        # Query the data
        result = db.query(V_Breakfast_Lunch).all()
        logger.info(f"Successfully fetched {len(result)} records")
        
        # Log the first record if any exists
        if result:
            first_record = result[0]
            logger.info(f"Sample record: {first_record.__dict__}")
        
        return result
    except Exception as e:
        logger.error(f"Error in get_veg_breakfast_lunch: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_v_breakfast_lunch(db: Session, v_breakfast_lunch_id: int):
    return db.query(V_Breakfast_Lunch).filter(V_Breakfast_Lunch.id == v_breakfast_lunch_id).first()

def update_v_breakfast_lunch(db: Session, v_breakfast_lunch: Veg_Breakfast_Lunch_Create, v_breakfast_lunch_id: int):
    v_breakfast_lunch_queryset = db.query(V_Breakfast_Lunch).filter(V_Breakfast_Lunch.id == v_breakfast_lunch_id).first()
    if v_breakfast_lunch_queryset:
        for key, value in v_breakfast_lunch.model_dump().items():
            setattr(v_breakfast_lunch_queryset, key, value)
        db.commit()
        db.refresh(v_breakfast_lunch_queryset)
    return v_breakfast_lunch_queryset


def delete_veg_breakfast_lunch(db: Session, veg_breakfast_lunch_id: int):
    v_breakfast_lunch_queryset = db.query(V_Breakfast_Lunch).filter(V_Breakfast_Lunch.id == veg_breakfast_lunch_id).first()
    if not v_breakfast_lunch_queryset:
        return None

    db.delete(v_breakfast_lunch_queryset)
    db.commit()
    return v_breakfast_lunch_queryset

