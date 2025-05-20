from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Meals, AdditionalService
from schemas import Meal, AdditionalService as AdditionalServiceSchema
from services import get_meals, get_services
from sqlalchemy import text
from decimal import Decimal
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from routes import router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(router)

class UserDetails(BaseModel):
    food_type: str  # Changed from dietary_preference
    plan_type: str  # Changed from purpose
    num_people: int  # Changed from people_count
    basic_details: str  # Changed from meals
    frequency: str = "8 Times/Month"  # Added default
    duration: str = "1.5 Hour"  # Added default
    kitchen_platform: bool

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
        # Use the actual number of people for the price column
        price_col = f"price_{num_people}"

        # Get base price
        base_query = text("""
            SELECT basic_price FROM meals 
            WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
            AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type)) 
            AND num_people=:num_people 
            AND LOWER(TRIM(basic_details))=LOWER(TRIM(:meal_type))
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
        total = Decimal(str(base_price))

        # Get additional services
        if services:
            # Normalize food type for comparison
            normalized_food_type = food_type.replace(" - ", "-").replace(" -", "-").replace("- ", "-")
            print(f"\nDEBUG: Food Type Normalization:")
            print(f"Original food_type: {food_type}")
            print(f"Normalized food_type: {normalized_food_type}")
            
            placeholders = ', '.join([':service' + str(i) for i in range(len(services))])
            add_query = text(f"""
                SELECT DISTINCT ON (code) code, name, is_percentage, {price_col} as price 
                FROM additional_services 
                WHERE (
                    LOWER(TRIM(food_type)) = LOWER(TRIM(:food_type))
                    OR LOWER(TRIM(REPLACE(food_type, ' - ', '-'))) = LOWER(TRIM(:food_type))
                    OR LOWER(TRIM(REPLACE(:food_type, ' - ', '-'))) = LOWER(TRIM(food_type))
                    OR LOWER(TRIM(food_type)) = LOWER(TRIM(:normalized_food_type))
                )
                AND LOWER(TRIM(plan_type)) = LOWER(TRIM(:plan_type))
                AND code IN ({placeholders})
                ORDER BY code
            """)
            
            params = {
                "food_type": food_type,
                "normalized_food_type": normalized_food_type,
                "plan_type": plan_type
            }
            params.update({f"service{i}": service for i, service in enumerate(services)})
            
            try:
                print(f"\nDEBUG: Query being executed:")
                print(f"SQL: {add_query}")
                print(f"Parameters: {params}")
                print(f"Price column being used: {price_col}")
                
                # First, let's check if the service exists with these parameters
                check_query = text("""
                    SELECT code, name, food_type, {price_col} as price
                    FROM additional_services 
                    WHERE code = :service0
                    ORDER BY {price_col}
                """.format(price_col=price_col))
                
                check_results = db.execute(check_query, {
                    "service0": services[0]
                }).fetchall()
                
                print("\nDEBUG: Available services in database:")
                for row in check_results:
                    print(f"Code: {row[0]}, Name: {row[1]}, Food Type: {row[2]}, Price: {row[3]}")
                
                results = db.execute(add_query, params).fetchall()
                print(f"\nQuery results: {results}")
                print(f"Number of services found: {len(results)}")

                if not results:
                    print("WARNING: No additional services found in database for the given parameters")
                    print(f"Food type: {normalized_food_type}")
                    print(f"Plan type: {plan_type}")
                    print(f"Meal type: {meal_type}")
                    print(f"Services requested: {services}")
                    return {
                        "base_price": round(Decimal(str(base_price)), 2),
                        "total_price": round(Decimal(str(base_price)), 2),
                        "num_people": num_people,
                        "food_type": food_type,
                        "plan_type": plan_type,
                        "meal_type": meal_type,
                        "services": services,
                        "message": "No matching services found"
                    }

                print(f"\nDEBUG: Price Calculation Details:")
                print(f"Base Price: {base_price}")
                total = Decimal(str(base_price))
                print(f"Initial Total: {total}")

                for row in results:
                    code, name, is_percent, price = row
                    print(f"\nProcessing service {code} ({name}):")
                    print(f"Is Percentage: {is_percent}")
                    print(f"Price Value: {price}")
                    
                    if is_percent:
                        service_amount = (total * Decimal(str(price)) / Decimal('100'))
                        print(f"Percentage Calculation: {total} * {price}% = {service_amount}")
                        total += service_amount
                    else:
                        print(f"Adding Fixed Amount: {price}")
                        total += Decimal(str(price))
                    
                    print(f"Running Total: {total}")

                print(f"\nFinal Total: {total}")
                print(f"Rounded Total: {round(total, 2)}")

                return {
                    "base_price": round(Decimal(str(base_price)), 2),
                    "total_price": round(total, 2),
                    "num_people": num_people,
                    "food_type": food_type,
                    "plan_type": plan_type,
                    "meal_type": meal_type,
                    "services": services
                }
            except Exception as e:
                print(f"ERROR: {str(e)}")
                print(f"Error type: {type(e)}")
                import traceback
                print(f"Traceback: {traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/save_details")
async def save_details(details: UserDetails, db: Session = Depends(get_db)):
    try:
        # Store the details in the database or session
        # For now, we'll just validate and process the data
        if details.num_people < 1 or details.num_people > 10:
            raise HTTPException(status_code=400, detail="Number of people must be between 1 and 10")
        
        # Convert food type to match database format
        food_type = details.food_type.replace(" - ", "-").strip()
        
        # Get meal plans based on the details
        meal_plans = db.query(Meals).filter(
            Meals.food_type.ilike(f"%{food_type}%"),
            Meals.num_people == details.num_people
        ).all()
        
        if not meal_plans:
            raise HTTPException(
                status_code=404,
                detail=f"No meal plans found for {food_type} with {details.num_people} people"
            )
        
        # Calculate base price considering kitchen platform
        base_price = Decimal('0')
        for meal in meal_plans:
            base_price += meal.basic_price
        
        # Add kitchen platform cleaning cost if selected
        if details.kitchen_platform:
            kitchen_service = db.query(AdditionalService).filter(
                AdditionalService.code == 'KP',
                AdditionalService.food_type.ilike(f"%{food_type}%")
            ).first()
            
            if kitchen_service:
                price_field = getattr(kitchen_service, f'price_{details.num_people}')
                if kitchen_service.is_percentage:
                    base_price += (base_price * price_field / 100)
                else:
                    base_price += price_field
        
        return {
            "status": "success",
            "data": {
                "food_type": details.food_type,
                "plan_type": details.plan_type,
                "num_people": details.num_people,
                "basic_details": details.basic_details,
                "frequency": details.frequency,
                "duration": details.duration,
                "kitchen_platform": details.kitchen_platform,
                "base_price": float(base_price),
                "available_plans": len(meal_plans)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/meals", response_model=List[Meal])
def get_meals_endpoint(
    food_type: str = Query(..., description="Food type (vegetarian/non-vegetarian)"),
    num_people: int = Query(..., ge=1, le=10, description="Number of people (1-10)"),
    db: Session = Depends(get_db)
):
    try:
        # Clean up the food_type to match database format
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

if __name__ == "__main__":
    # Configure logging
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


