from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/meals/", response_model=List[schemas.Meal])
def get_meals(
    db: Session = Depends(get_db)
):
    meals = db.query(models.Meals).all()
    return meals

@router.get("/additional-services/", response_model=List[schemas.AdditionalService])
def get_additional_services(
    num_people: int,
    db: Session = Depends(get_db)
):
    services = db.query(models.AdditionalService).all()
    return services

@router.post("/calculate-price/")
def calculate_price(
    request: schemas.PriceCalculationRequest,
    db: Session = Depends(get_db)
):
    # Get meal
    meal = db.query(models.Meals).filter(
        models.Meals.id == request.meal_id
    ).first()
    
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    # Get additional services
    services = db.query(models.AdditionalService).filter(
        models.AdditionalService.id.in_(request.service_ids)
    ).all()
    
    # Calculate total price
    total_price = meal.basic_price
    for service in services:
        # Get the appropriate price based on number of people
        price_field = getattr(service, f'price_{meal.num_people}')
        if service.is_percentage:
            total_price += (meal.basic_price * price_field / 100)
        else:
            total_price += price_field
    
    return {
        "meal_price": meal.basic_price,
        "services_price": sum(
            getattr(service, f'price_{meal.num_people}') if not service.is_percentage 
            else (meal.basic_price * getattr(service, f'price_{meal.num_people}') / 100)
            for service in services
        ),
        "total_price": total_price
    }

@router.post("/meals/", response_model=schemas.Meal)
def create_meal(
    meal: schemas.MealCreate,
    db: Session = Depends(get_db)
):
    try:
        db_meal = models.Meals(
            food_type=meal.food_type,
            plan_type=meal.plan_type,
            num_people=meal.num_people,
            basic_price=meal.basic_price,
            basic_details=meal.basic_details,
            frequency=meal.frequency,
            duration=meal.duration
        )
        
        # Add additional services if any
        if meal.service_ids:
            services = db.query(models.AdditionalService).filter(
                models.AdditionalService.id.in_(meal.service_ids)
            ).all()
            
            if len(services) != len(meal.service_ids):
                raise HTTPException(
                    status_code=400,
                    detail="One or more service IDs are invalid"
                )
            
            db_meal.additional_services = services

        db.add(db_meal)
        db.commit()
        db.refresh(db_meal)
        return db_meal
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calculate-total")
def calculate_total(
    food_type: str = Query(..., description="Food type (VEG/NON_VEG)"),
    plan_type: str = Query(..., description="Plan type (BASIC/STANDARD/PREMIUM)"),
    num_people: int = Query(..., ge=1, le=7, description="Number of people (1-7)"),
    meal_type: str = Query(..., description="Meal type (BREAKFAST/LUNCH/DINNER/etc)"),
    services: List[str] = Query([], description="List of service codes (A/B/C/D)"),
    db: Session = Depends(get_db)
):
    try:
        num_key = min(num_people, 7)
        price_col = f"price_{num_key}"

        # Get base price
        base_query = text("""
            SELECT basic_price FROM meals 
            WHERE food_type=:food_type AND plan_type=:plan_type AND num_people=:num_people AND basic_details=:meal_type
        """)
        base_result = db.execute(base_query, {
            "food_type": food_type,
            "plan_type": plan_type,
            "num_people": num_people,
            "meal_type": meal_type
        }).fetchone()
        
        if not base_result:
            raise HTTPException(
                status_code=404, 
                detail=f"No meal plan found for food_type={food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}"
            )
            
        base_price = base_result[0]
        total = base_price

        # Get additional services
        if services:
            placeholders = ', '.join([':service' + str(i) for i in range(len(services))])
            add_query = text(f"""
                SELECT code, is_percentage, {price_col} FROM additional_serives
                WHERE food_type=:food_type AND plan_type=:plan_type AND meal_combo=:meal_type AND code IN ({placeholders})
            """)
            
            params = {
                "food_type": food_type,
                "plan_type": plan_type,
                "meal_type": meal_type
            }
            params.update({f"service{i}": service for i, service in enumerate(services)})
            
            results = db.execute(add_query, params).fetchall()

            for code, is_percent, price in results:
                if is_percent:
                    total += (base_price * price / 100)
                else:
                    total += price

        return {
            "base_price": round(base_price, 2),
            "total_price": round(total, 2),
            "num_people": num_people,
            "food_type": food_type,
            "plan_type": plan_type,
            "meal_type": meal_type,
            "services": services
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 