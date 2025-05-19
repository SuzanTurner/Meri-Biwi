from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Meals, AdditionalService
from schemas import Meal, AdditionalService as AdditionalServiceSchema
from services import get_meals, get_services
from sqlalchemy import text

app = FastAPI()

@app.get("/meals", response_model=List[Meal])
def get_meals_endpoint(db: Session = Depends(get_db)):
    try:
        meals = get_meals(db)
        return meals
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching meals: {str(e)}")

@app.get("/additional-services", response_model=List[AdditionalServiceSchema])
def get_additional_services_endpoint(db: Session = Depends(get_db)):
    try:
        services = get_services(db)
        return services
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching additional services: {str(e)}")

@app.get("/calculate_total")
def calculate_total(
    food_type: str,
    plan_type: str,
    num_people: int,
    meal_type: str,
    services: List[str] = Query([]),
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
                SELECT code, is_percentage, {price_col} FROM additional_services
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


