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
    food_type: str,
    num_people: int,
    db: Session = Depends(get_db)
):
    meals = db.query(models.Meals).filter(models.Meals.food_type == food_type, models.Meals.num_people == num_people).all()
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
        db_food_type = food_type
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
                SELECT DISTINCT ON (code) code, name, is_percentage, price_{num_people} as price 
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
                "food_type": db_food_type,
                "normalized_food_type": db_food_type.replace(" - ", "-").replace(" -", "-").replace("- ", "-"),
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

@router.post("/api/save_details")
def save_details(
    details: schemas.UserDetails,
    db: Session = Depends(get_db)
):
    try:
        logger.info("=== Saving User Details ===")
        logger.info(f"Received details: {details.dict()}")

        # Convert food type to match database format
        db_food_type = details.food_type
        if db_food_type.lower() in ["vegetarian", "veg"]:
            db_food_type = "Veg"
        elif db_food_type.lower() in ["non-vegetarian", "non vegetarian", "non veg", "non-veg", "non veg", "Non-Veg", "Non-veg", "Non-Vegetarian", "Non-vegetarian", "Non - Veg", "Non - veg", "Non - Vegetarian", "Non - Vegetarian"]:
            db_food_type = "Non - Veg"  # Ensure consistent format with spaces around hyphen
        
        logger.info(f"=== Food Type Conversion ===")
        logger.info(f"Original food type: '{details.food_type}'")
        logger.info(f"Converted food type: '{db_food_type}'")
        
        # Debug: Check all meal plans in database
        all_meals_query = text("""
            SELECT food_type, plan_type, num_people, basic_details 
            FROM meals 
            ORDER BY food_type, plan_type, num_people
        """)
        all_meals = db.execute(all_meals_query).fetchall()
        logger.info("=== Available Meal Plans in Database ===")
        for meal in all_meals:
            logger.info(f"Meal: food_type='{meal[0]}', plan_type='{meal[1]}', num_people={meal[2]}, details='{meal[3]}'")
        
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

        # Get base price with exact matching
        base_query = text("""
            SELECT * FROM meals 
            WHERE food_type = :food_type 
            AND plan_type = :plan_type 
            AND num_people = :num_people 
            AND basic_details = :meal_type
        """)
        
        params = {
            "food_type": db_food_type,
            "plan_type": plan_type,
            "num_people": details.num_people,
            "meal_type": details.basic_details
        }
        
        logger.info("=== Query Parameters ===")
        logger.info(f"food_type: '{params['food_type']}'")
        logger.info(f"plan_type: '{params['plan_type']}'")
        logger.info(f"num_people: {params['num_people']}")
        logger.info(f"meal_type: '{params['meal_type']}'")
        
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
    
@router.get("/cleaning", response_model=List[schemas.Cleaning])
def get_cleaning_plans(
    floor: Optional[int] = None,
    plan: Optional[str] = None,
    bhk: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        logger.info("=== Fetching Cleaning Plans ===")
        logger.info(f"Parameters: floor={floor}, plan={plan}, bhk={bhk}")
        
        query = db.query(models.Cleaning)
        
        if floor is not None:
            # Format floor parameter to match database format
            floor_str = f"Floor {floor}"
            logger.info(f"Formatted floor parameter: {floor_str}")
            query = query.filter(models.Cleaning.floor == floor_str)
            
        if plan:
            # Normalize plan parameter
            plan = plan.strip().capitalize()
            logger.info(f"Normalized plan parameter: {plan}")
            query = query.filter(models.Cleaning.plan == plan)
            
        if bhk is not None:
            query = query.filter(models.Cleaning.bhk == bhk)
            
        cleaning_plans = query.all()
        logger.info(f"Found {len(cleaning_plans)} cleaning plans")
        
        if not cleaning_plans:
            logger.warning("No cleaning plans found with the given parameters")
            
        return cleaning_plans
        
    except Exception as e:
        logger.error(f"Error in get_cleaning_plans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/additional-cleaning", response_model=List[schemas.AdditionalCleaningPlan])
def get_additional_cleaning_plans(
    code: Optional[str] = None,
    plan: Optional[str] = None,
    floor: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        logger.info("=== Fetching Additional Cleaning Plans ===")
        logger.info(f"Parameters: code={code}, plan={plan}, floor={floor}")
        
        query = db.query(models.AdditionalCleaningPlan)
        
        if code:
            # Normalize code parameter (A, B, or C)
            code = code.strip().upper()
            logger.info(f"Normalized code parameter: {code}")
            if code not in ['A', 'B', 'C']:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid code. Must be one of: A, B, C"
                )
            query = query.filter(models.AdditionalCleaningPlan.code == code)
            
        if plan:
            # Normalize plan parameter
            plan = plan.strip().capitalize()
            logger.info(f"Normalized plan parameter: {plan}")
            query = query.filter(models.AdditionalCleaningPlan.plan == plan)
            
        if floor is not None:
            # Format floor parameter to match database format
            floor_str = f"Floor {floor}"
            logger.info(f"Formatted floor parameter: {floor_str}")
            query = query.filter(models.AdditionalCleaningPlan.floor == floor_str)
            
        additional_plans = query.all()
        logger.info(f"Found {len(additional_plans)} additional cleaning plans")
        
        if not additional_plans:
            logger.warning("No additional cleaning plans found with the given parameters")
            
        return additional_plans
        
    except Exception as e:
        logger.error(f"Error in get_additional_cleaning_plans: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calculate-cleaning-total")
def calculate_cleaning_total(
    floor: int = Query(..., ge=1, le=10, description="Floor number (1-10)"),
    plan: str = Query(..., description="Plan type (Basic/Standard/Premium)"),
    bhk: int = Query(..., ge=1, le=5, description="BHK (1-5)"),
    bathrooms: int = Query(1, ge=1, le=5, description="Number of bathrooms (1-5)"),
    services: List[str] = Query([], description="List of additional service codes (A/B/C)"),
    db: Session = Depends(get_db)
):
    try:
        logger.info("=== Request Details ===")
        logger.info(f"Query Parameters: floor={floor}, plan={plan}, bhk={bhk}, bathrooms={bathrooms}, services={services}")
        
        # Format floor for database query
        floor_str = f"Floor {floor}"
        
        # Get base price
        base_query = text("""
            SELECT price FROM cleaning 
            WHERE LOWER(TRIM(plan)) = LOWER(TRIM(:plan)) 
            AND bhk = :bhk
            AND LOWER(TRIM(floor)) = LOWER(TRIM(:floor))
        """)
        
        logger.info("Executing base price query with parameters:")
        logger.info(f"plan={plan}, bhk={bhk}, floor={floor_str}")
        
        base_result = db.execute(base_query, {
            "plan": plan,
            "bhk": bhk,
            "floor": floor_str
        }).fetchone()
        
        if not base_result:
            logger.error("No matching cleaning plan found")
            raise HTTPException(
                status_code=404,
                detail=f"No cleaning plan found for floor={floor}, plan={plan}, bhk={bhk}"
            )
        
        base_price = base_result[0]
        total = Decimal(str(base_price))
        logger.info(f"Base price: {base_price}")
        
        # Get additional services if any
        if services:
            # Convert services to a set to ensure uniqueness
            unique_services = set(services)
            
            # Validate service codes
            invalid_codes = [c for c in unique_services if c not in ['A', 'B', 'C']]
            if invalid_codes:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid service codes: {invalid_codes}. Must be one of: A, B, C"
                )
            
            bathroom_col = f"bathroom_{bathrooms}"
            placeholders = ', '.join([':service' + str(i) for i in range(len(unique_services))])
            add_query = text(f"""
                SELECT DISTINCT ON (code) code, service_name, {bathroom_col} as price 
                FROM additional_cleaning 
                WHERE LOWER(TRIM(plan)) = LOWER(TRIM(:plan))
                AND LOWER(TRIM(floor)) = LOWER(TRIM(:floor))
                AND code IN ({placeholders})
                ORDER BY code
            """)
            
            params = {
                "plan": plan,
                "floor": floor_str
            }
            params.update({f"service{i}": service for i, service in enumerate(unique_services)})
            
            logger.info("Executing additional services query with parameters:")
            logger.info(f"Query: {add_query}")
            logger.info(f"Parameters: {params}")
            
            results = db.execute(add_query, params).fetchall()
            
            logger.info("Additional services found:")
            # Track processed services to prevent duplicates
            processed_services = set()
            
            for code, name, price in results:
                # Skip if we've already processed this service
                if code in processed_services:
                    logger.info(f"Skipping duplicate service: {code}")
                    continue
                    
                processed_services.add(code)
                logger.info(f"Service: {code} ({name})")
                logger.info(f"Price: {price}")
                
                if code == 'C':  # Only code 'C' is percentage
                    service_amount = (total * Decimal(str(price)) / Decimal('100'))
                    logger.info(f"Percentage calculation: {total} * {price}% = {service_amount}")
                    total += service_amount
                else:
                    logger.info(f"Adding fixed amount: {price}")
                    total += Decimal(str(price))
                
                logger.info(f"Running total: {total}")
        
        response = {
            "base_price": float(base_price),
            "total_price": float(total),
            "floor": floor_str,
            "plan": plan,
            "bhk": bhk,
            "bathrooms": bathrooms,
            "services": services
        }
        
        logger.info("=== Response ===")
        logger.info(json.dumps(response, indent=2))
        
        return response
        
    except Exception as e:
        logger.error(f"Error in calculate_cleaning_total: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

