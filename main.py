from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Meals, AdditionalService, Cleaning, AdditionalCleaningPlan
from schemas import (
    Meal, 
    AdditionalService as AdditionalServiceSchema, 
    Cleaning as CleaningSchema, 
    AdditionalCleaningPlan as AdditionalCleaningPlanSchema,
    CleaningTotalResponse
)
from services import get_meals, get_services, get_cleaning_plans, get_additional_cleaning_plans
from sqlalchemy import text
from decimal import Decimal
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes import router
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(name)s:%(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI(debug=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

class UserDetails(BaseModel):
    food_type: str
    plan_type: str
    num_people: int
    basic_details: str
    frequency: str = "8 Times/Month"
    duration: str = "1.5 Hour"
    kitchen_platform: bool

class CleaningDetails(BaseModel):
    floor: int
    plan: str
    bhk: int
    bathrooms: int
    code: List[str] = []
    purpose: str

@app.get("/meals", response_model=List[Meal])
def get_meals_endpoint(
    food_type: str = Query(..., description="Food type (vegetarian/non-vegetarian)"),
    num_people: int = Query(..., ge=1, le=10, description="Number of people (1-10)"),
    db: Session = Depends(get_db)
):
    try:
        food_type = food_type.replace(" - ", "-").strip()
        meals = db.query(Meals).filter(
            Meals.food_type.ilike(f"%{food_type}%"),
            Meals.num_people == num_people
        ).all()
        
        if not meals:
            raise HTTPException(
                status_code=404,
                detail=f"No meal plans found for {food_type} with {num_people} people"
            )
        
        return meals
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching meals: {str(e)}")

@app.get("/additional-services", response_model=List[AdditionalServiceSchema])
def get_additional_services_endpoint(db: Session = Depends(get_db)):
    try:
        services = get_services(db)
        return services
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching additional services: {str(e)}")

@app.get("/cleaning", response_model=List[CleaningSchema])
def get_cleaning_plans_endpoint(
    floor: int = Query(None, ge=1, le=10, description="Floor number (1-10)"),
    plan: str = Query(None, description="Plan type (Basic/Standard/Premium)"),
    bhk: int = Query(None, ge=1, le=5, description="BHK (1-5)"),
    db: Session = Depends(get_db)
):
    try:
        cleaning_plans = get_cleaning_plans(db, floor, plan, bhk)
        return cleaning_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching cleaning plans: {str(e)}")

@app.get("/additional-cleaning", response_model=List[AdditionalCleaningPlanSchema])
def get_additional_cleaning_plans_endpoint(
    code: str = Query(None, description="Service code (A/B/C)"),
    plan: str = Query(None, description="Plan type (Basic/Standard/Premium)"),
    floor: int = Query(None, ge=1, le=10, description="Floor number (1-10)"),
    db: Session = Depends(get_db)
):
    try:
        additional_plans = get_additional_cleaning_plans(db, code, plan, floor)
        return additional_plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching additional cleaning plans: {str(e)}")

@app.get("/calculate-cleaning-total", response_model=CleaningTotalResponse)
def calculate_cleaning_total(
    floor: int = Query(..., ge=1, le=10, description="Floor number (1-10)"),
    plan: str = Query(..., description="Plan type (Basic/Standard/Premium)"),
    bhk: int = Query(..., ge=1, le=5, description="BHK (1-5)"),
    bathrooms: int = Query(1, ge=1, le=5, description="Number of bathrooms (1-5)"),
    services: List[str] = Query([], description="List of additional service codes (A/B/C)"),
    db: Session = Depends(get_db)
):
    try:
        # Get base price
        base_query = text("""
            SELECT price FROM cleaning 
            WHERE LOWER(TRIM(plan))=LOWER(TRIM(:plan)) 
            AND bhk=:bhk
        """)
        
        base_result = db.execute(base_query, {
            "plan": plan,
            "bhk": bhk
        }).fetchone()
        
        if not base_result:
            raise HTTPException(
                status_code=404,
                detail=f"No cleaning plan found for plan={plan}, bhk={bhk}"
            )
            
        base_price = base_result[0]
        total = Decimal(str(base_price))

        # Get additional services if any
        if services:
            bathroom_col = f"bathroom_{bathrooms}"
            placeholders = ', '.join([':service' + str(i) for i in range(len(services))])
            add_query = text(f"""
                SELECT DISTINCT ON (code) code, service_name, {bathroom_col} as price 
                FROM additional_cleaning 
                WHERE LOWER(TRIM(plan))=LOWER(TRIM(:plan))
                AND LOWER(TRIM(floor))=LOWER(TRIM(:floor))
                AND code IN ({placeholders})
                ORDER BY code
            """)
            
            params = {
                "plan": plan,
                "floor": f"Floor {floor}"
            }
            params.update({f"service{i}": service for i, service in enumerate(services)})
            
            results = db.execute(add_query, params).fetchall()
            
            # Track processed services to prevent duplicates
            processed_services = set()
            
            for code, name, price in results:
                if code in processed_services:
                    continue
                    
                processed_services.add(code)
                
                if code == 'C':  # Only code 'C' is percentage
                    service_amount = (total * Decimal(str(price)) / Decimal('100'))
                    total += service_amount
                else:
                    total += Decimal(str(price))

        return {
            "base_price": float(base_price),
            "total_price": float(total),
            "floor": f"Floor {floor}",
            "plan": plan,
            "bhk": bhk,
            "bathrooms": bathrooms,
            "services": services
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in calculate_cleaning_total: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


