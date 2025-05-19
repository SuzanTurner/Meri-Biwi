from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Meals, AdditionalService
from schemas import Meal, AdditionalService as AdditionalServiceSchema
from services import get_meals, get_services
from sqlalchemy import text
from decimal import Decimal

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
            # Clean up the food_type to match database format
            food_type = food_type.replace(" - ", "-").strip()
            
            placeholders = ', '.join([':service' + str(i) for i in range(len(services))])
            add_query = text(f"""
                SELECT DISTINCT ON (code) code, name, is_percentage, {price_col} as price 
                FROM additional_services 
                WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
                AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type))
                AND code IN ({placeholders})
                ORDER BY code
            """)
            
            params = {
                "food_type": food_type,
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
                    SELECT code, name, {price_col} as price
                    FROM additional_services 
                    WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
                    AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type))
                    AND code = :service0
                    ORDER BY {price_col}
                """.format(price_col=price_col))
                
                check_results = db.execute(check_query, {
                    "food_type": food_type,
                    "plan_type": plan_type,
                    "service0": services[0]
                }).fetchall()
                
                print("\nDEBUG: Available services in database:")
                for row in check_results:
                    print(f"Code: {row[0]}, Name: {row[1]}, Price: {row[2]}")
                
                results = db.execute(add_query, params).fetchall()
                print(f"\nQuery results: {results}")
                print(f"Number of services found: {len(results)}")

                if not results:
                    print("WARNING: No additional services found in database for the given parameters")
                    print(f"Food type: {food_type}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


