from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas
from database import get_db
from sqlalchemy import text
from enum import Enum
import json
import logging
from decimal import Decimal

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class FoodType(str, Enum):
    VEG = "Veg"
    NON_VEG = "Non - Veg"

class PlanType(str, Enum):
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"

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
            basic_details=meal.basic_details
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

@router.get("/calculate_total")
def calculate_total(
    food_type: str,
    plan_type: str,
    num_people: int,
    meal_type: str,
    services: List[str] = Query([]),
    db: Session = Depends(get_db)
):
    try:
        logger.info("=== Request Details ===")
        logger.info(f"Query Parameters: food_type={food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}")
        
        # Convert food type to match database format
        db_food_type = food_type.replace(" - ", "-").strip()
        logger.info(f"Converted food_type to: {db_food_type}")
        
        # Get base price
        base_query = text("""
            SELECT basic_price FROM meals 
            WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
            AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type)) 
            AND num_people=:num_people 
            AND LOWER(TRIM(basic_details))=LOWER(TRIM(:meal_type))
        """)
        
        logger.info("Executing base price query with parameters:")
        logger.info(f"food_type={db_food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}")
        
        base_result = db.execute(base_query, {
            "food_type": db_food_type,
            "plan_type": plan_type,
            "num_people": num_people,
            "meal_type": meal_type
        }).fetchone()
        
        if not base_result:
            logger.error("No matching meal plan found")
            raise HTTPException(
                status_code=404,
                detail=f"No meal plan found for food_type={db_food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}"
            )
        
        base_price = base_result[0]
        total = Decimal(str(base_price))
        
        # Get additional services if any
        if services:
            # Convert services to a set to ensure uniqueness
            unique_services = set(services)
            
            placeholders = ', '.join([':service' + str(i) for i in range(len(unique_services))])
            add_query = text(f"""
                SELECT code, name, is_percentage, price_{num_people} as price 
                FROM additional_services 
                WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
                AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type))
                AND code IN ({placeholders})
            """)
            
            params = {
                "food_type": db_food_type,
                "plan_type": plan_type
            }
            params.update({f"service{i}": service for i, service in enumerate(unique_services)})
            
            logger.info("Executing additional services query with parameters:")
            logger.info(f"Query: {add_query}")
            logger.info(f"Parameters: {params}")
            
            results = db.execute(add_query, params).fetchall()
            
            logger.info("Additional services found:")
            # Track processed services to prevent duplicates
            processed_services = set()
            
            for code, name, is_percent, price in results:
                # Skip if we've already processed this service
                if code in processed_services:
                    logger.info(f"Skipping duplicate service: {code}")
                    continue
                    
                processed_services.add(code)
                logger.info(f"Service: {code} ({name})")
                logger.info(f"Is Percentage: {is_percent}")
                logger.info(f"Price: {price}")
                
                if is_percent:
                    service_amount = (base_price * Decimal(str(price)) / Decimal('100'))
                    logger.info(f"Percentage calculation: {base_price} * {price}% = {service_amount}")
                    total += service_amount
                else:
                    logger.info(f"Adding fixed amount: {price}")
                    total += Decimal(str(price))
                
                logger.info(f"Running total: {total}")
        
        response = {
            "base_price": float(base_price),
            "total_price": float(total),
            "num_people": num_people,
            "food_type": db_food_type,
            "plan_type": plan_type,
            "meal_type": meal_type,
            "services": services
        }
        
        logger.info("=== Response ===")
        logger.info(json.dumps(response, indent=2))
        
        return response
        
    except Exception as e:
        logger.error(f"Error in calculate_total: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save_details")
def save_details(
    details: schemas.UserDetails,
    db: Session = Depends(get_db)
):
    try:
        logger.info("=== Saving User Details ===")
        logger.info(f"Received details: {details.dict()}")

        # Debug: Check all meal plans in database
        all_meals_query = text("""
            SELECT * FROM meals 
            ORDER BY food_type, plan_type, num_people
        """)
        all_meals = db.execute(all_meals_query).fetchall()
        logger.info("=== All Meal Plans in Database ===")
        for meal in all_meals:
            logger.info(f"Meal: {meal}")

        # Convert food type to match database format
        db_food_type = FoodType.VEG.value if details.food_type.lower() in ["vegetarian", "veg"] else FoodType.NON_VEG.value
        
        # Convert plan type to match database format
        plan_type = details.plan_type.capitalize()
        if plan_type not in [pt.value for pt in PlanType]:
            logger.error(f"Invalid plan type: {plan_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid plan type. Must be one of: {', '.join([pt.value for pt in PlanType])}"
            )

        # Validate number of people
        if not 1 <= details.num_people <= 7:
            logger.error(f"Invalid number of people: {details.num_people}")
            raise HTTPException(
                status_code=400,
                detail="Number of people must be between 1 and 7"
            )

        # Validate meal type format
        valid_meal_types = [
            "3 Meals {Breakfast+Tea & Lunch + Dinner}",
            "2 Meals {Breakfast+Tea & Lunch}",
            "1 Meal Lunch",
            "1 Meal Dinner"
        ]
        
        if details.basic_details not in valid_meal_types:
            logger.warning(f"Invalid meal type: {details.basic_details}, defaulting to 2 Meals")
            details.basic_details = "2 Meals {Breakfast+Tea & Lunch}"

        # Get base price
        base_query = text("""
            SELECT * FROM meals 
            WHERE food_type=:food_type 
            AND plan_type=:plan_type 
            AND num_people=:num_people 
            AND basic_details=:meal_type
        """)
        
        params = {
            "food_type": db_food_type,
            "plan_type": plan_type,
            "num_people": details.num_people,
            "meal_type": details.basic_details
        }
        
        logger.info("=== Query Parameters ===")
        logger.info(f"food_type: {db_food_type}")
        logger.info(f"plan_type: {plan_type}")
        logger.info(f"num_people: {details.num_people}")
        logger.info(f"meal_type: {details.basic_details}")
        
        base_result = db.execute(base_query, params).fetchone()
        
        if not base_result:
            logger.error("No matching meal plan found")
            logger.error(f"Query parameters: {params}")
            raise HTTPException(
                status_code=404,
                detail=f"No meal plan found for food_type={db_food_type}, plan_type={plan_type}, num_people={details.num_people}, meal_type={details.basic_details}"
            )

        # Return success response with the details
        response = {
            "status": "success",
            "data": {
                "food_type": db_food_type,
                "plan_type": plan_type,
                "num_people": details.num_people,
                "basic_details": details.basic_details,
                "base_price": float(base_result.basic_price),
                "available_plans": 24  # This could be calculated based on available plans
            }
        }

        logger.info("=== Response ===")
        logger.info(json.dumps(response, indent=2))

        return response

    except Exception as e:
        logger.error(f"Error in save_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

        # Convert food type to match database format
        db_food_type = FoodType.VEG.value if details.food_type.lower() in ["vegetarian", "veg"] else FoodType.NON_VEG.value
        
        # Convert plan type to match database format
        plan_type = details.plan_type.capitalize()
        if plan_type not in [pt.value for pt in PlanType]:
            logger.error(f"Invalid plan type: {plan_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid plan type. Must be one of: {', '.join([pt.value for pt in PlanType])}"
            )

        # Validate number of people
        if not 1 <= details.num_people <= 7:
            logger.error(f"Invalid number of people: {details.num_people}")
            raise HTTPException(
                status_code=400,
                detail="Number of people must be between 1 and 7"
            )

        # Validate meal type format
        valid_meal_types = [
            "3 Meals {Breakfast+Tea & Lunch + Dinner}",
            "2 Meals {Breakfast+Tea & Lunch}",
            "1 Meal Lunch",
            "1 Meal Dinner"
        ]
        
        if details.basic_details not in valid_meal_types:
            logger.warning(f"Invalid meal type: {details.basic_details}, defaulting to 2 Meals")
            details.basic_details = "2 Meals {Breakfast+Tea & Lunch}"

        # Get base price
        base_query = text("""
            SELECT basic_price FROM meals 
            WHERE food_type=:food_type 
            AND plan_type=:plan_type 
            AND num_people=:num_people 
            AND basic_details=:meal_type
        """)
        
        base_result = db.execute(base_query, {
            "food_type": db_food_type,
            "plan_type": plan_type,
            "num_people": details.num_people,
            "meal_type": details.basic_details
        }).fetchone()

        if not base_result:
            logger.error("No matching meal plan found")
            raise HTTPException(
                status_code=404,
                detail=f"No meal plan found for the provided details"
            )

        # Return success response with the details
        response = {
            "status": "success",
            "data": {
                "food_type": db_food_type,
                "plan_type": plan_type,
                "num_people": details.num_people,
                "basic_details": details.basic_details,
                "base_price": float(base_result[0]),
                "available_plans": 24  # This could be calculated based on available plans
            }
        }

        logger.info("=== Response ===")
        logger.info(json.dumps(response, indent=2))

        return response

    except Exception as e:
        logger.error(f"Error in save_details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 