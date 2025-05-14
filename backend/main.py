from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import services
from db import engine, get_db, create_table

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/Veg_Breakfast_Lunch/", response_model=List[schemas.Veg_Breakfast_Lunch])
def get_veg_breakfast_lunch(db: Session = Depends(get_db)):
    return services.get_veg_breakfast_lunch(db)

@app.post("/Veg_Breakfast_Lunch/", response_model=schemas.Veg_Breakfast_Lunch)
def create_veg_breakfast_lunch(veg_breakfast_lunch: schemas.Veg_Breakfast_Lunch, db: Session = Depends(get_db)):
    return services.create_veg_breakfast_lunch(db, veg_breakfast_lunch)

@app.get("/Veg_Breakfast_Lunch/{veg_breakfast_lunch_id}", response_model=schemas.Veg_Breakfast_Lunch)
def get_veg_breakfast_lunch_by_id(veg_breakfast_lunch_id: int, db: Session = Depends(get_db)):
    return services.get_veg_breakfast_lunch_by_id(db, veg_breakfast_lunch_id)

@app.put("/Veg_Breakfast_Lunch/{veg_breakfast_lunch_id}", response_model=schemas.Veg_Breakfast_Lunch)
def update_veg_breakfast_lunch(veg_breakfast_lunch_id: int, veg_breakfast_lunch: schemas.Veg_Breakfast_Lunch, db: Session = Depends(get_db)):
    return services.update_veg_breakfast_lunch(db, veg_breakfast_lunch_id, veg_breakfast_lunch)

@app.delete("/Veg_Breakfast_Lunch/{veg_breakfast_lunch_id}", response_model=schemas.Veg_Breakfast_Lunch)
def delete_veg_breakfast_lunch(veg_breakfast_lunch_id: int, db: Session = Depends(get_db)):
    deleted_item = services.delete_veg_breakfast_lunch(db, veg_breakfast_lunch_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item

