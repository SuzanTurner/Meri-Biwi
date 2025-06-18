
from fastapi import APIRouter, Depends, Query, HTTPException, status
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from decimal import Decimal
# from sqlalchemy import func, or_
# from modals import Meal, AdditionalService
import logging
import json


router = APIRouter(
    tags = ['Cooking'],
    prefix = '/cooking'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# DO NOT TOUCH THIS!!!


# @router.get("/")
# def calculate_total_cooking(
#     food_type: str,
#     plan_type: str,
#     num_people: int,
#     meal_type: str,
#     services: List[str] = Query([]),
#     db: Session = Depends(get_db)
# ):
#     try:
#         logger.info("=== Request Details ===")
#         logger.info(f"Query Parameters: food_type={food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}")
        
        
#         food_type = food_type.strip().lower().replace(" ", "")
#         if "veg" in food_type and "non" not in food_type:
#             db_food_type = "Veg"
#         elif "non" in food_type:
#             db_food_type = "Non - Veg"
#         else:
#             raise HTTPException(status_code=400, detail="Unsupported food type")
        
#         logger.info(f"Converted food_type to: {db_food_type}")
        
#         # Get base price
#         base_query = text("""
#             SELECT basic_price FROM meals 
#             WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
#             AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type)) 
#             AND num_people=:num_people 
#             AND LOWER(TRIM(basic_details))=LOWER(TRIM(:meal_type))
#         """)
        
#         logger.info("Executing base price query with parameters:")
#         logger.info(f"food_type={db_food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}")
        
#         base_result = db.execute(base_query, {
#             "food_type": db_food_type,
#             "plan_type": plan_type,
#             "num_people": num_people,
#             "meal_type": meal_type
#         }).fetchone()
        
#         if not base_result:
#             logger.error("No matching meal plan found")
#             # raise HTTPException(
#             #     status_code=404,
#             #     detail=f"No meal plan found for food_type={db_food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}"
#             # )
#             return {"status" : "error", "message" : "missing or invalid parameters"}
        
#         base_price = base_result[0]
#         total = Decimal(str(base_price))
        
#         # Get additional services if any
#         if services:
#             # Convert services to a set to ensure uniqueness
#             unique_services = set(services)
            
#             placeholders = ', '.join([':service' + str(i) for i in range(len(unique_services))])
#             add_query = text(f"""
#                 SELECT DISTINCT ON (code) code, name, is_percentage, price_{num_people} as price 
#                 FROM additional_services 
#                 WHERE (
#                     LOWER(TRIM(food_type)) = LOWER(TRIM(:food_type))
#                     OR LOWER(TRIM(REPLACE(food_type, ' - ', '-'))) = LOWER(TRIM(:food_type))
#                     OR LOWER(TRIM(REPLACE(:food_type, ' - ', '-'))) = LOWER(TRIM(food_type))
#                     OR LOWER(TRIM(food_type)) = LOWER(TRIM(:normalized_food_type))
#                 )
#                 AND LOWER(TRIM(plan_type)) = LOWER(TRIM(:plan_type))
#                 AND code IN ({placeholders})
#                 ORDER BY code
#             """)
            
#             params = {
#                 "food_type": db_food_type,
#                 "normalized_food_type": db_food_type.replace(" - ", "-").replace(" -", "-").replace("- ", "-"),
#                 "plan_type": plan_type
#             }
#             params.update({f"service{i}": service for i, service in enumerate(unique_services)})
            
#             logger.info("Executing additional services query with parameters:")
#             logger.info(f"Query: {add_query}")
#             logger.info(f"Parameters: {params}")
            
#             results = db.execute(add_query, params).fetchall()
            
#             logger.info("Additional services found:")
#             # Track processed services to prevent duplicates
#             processed_services = set()
            
#             for code, name, is_percent, price in results:
#                 # Skip if we've already processed this service
#                 if code in processed_services:
#                     logger.info(f"Skipping duplicate service: {code}")
#                     continue
                    
#                 processed_services.add(code)
#                 logger.info(f"Service: {code} ({name})")
#                 logger.info(f"Is Percentage: {is_percent}")
#                 logger.info(f"Price: {price}")
                
#                 if is_percent:
#                     service_amount = (base_price * Decimal(str(price)) / Decimal('100'))
#                     logger.info(f"Percentage calculation: {base_price} * {price}% = {service_amount}")
#                     total += service_amount
#                 else:
#                     logger.info(f"Adding fixed amount: {price}")
#                     total += Decimal(str(price))
                
#                 logger.info(f"Running total: {total}")
        
#         response = {
#             "base_price": float(base_price),
#             "total_price": float(total),
#             "num_people": num_people,
#             "food_type": db_food_type,
#             "plan_type": plan_type,
#             "meal_type": meal_type,
#             "services": services
#         }
        
#         formatted_response = {
#             "status" : "success",
#             "message" : "packages fetched succesfully",
#             "packages" : {"package_type" : plan_type,
#                           "icon" : "Some icon bro",
#                           "package_id" : "STD6969",
#                           "price" : float(total)},
#             "features" : response   
#         }
        
#         logger.info("=== Response ===")
#         logger.info(json.dumps(response, indent=2))
        
#         return formatted_response
        
#     except Exception as e:
#         logger.error(f"Error in calculate_total: {str(e)}")
#         return {"status" : "error", "message" : "missing or invalid parameters"}


# @router.get("/")
# def calculate_total_cooking(
#     food_type: str,
#     plan_type: str,
#     num_people: int,
#     meal_type: str,
#     services: List[str] = Query([]),
#     db: Session = Depends(get_db)
# ):
#     try:
#         logger.info("=== Request Details ===")
#         logger.info(f"Query Parameters: food_type={food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}")
        
        
#         food_type = food_type.strip().lower().replace(" ", "")
#         if "veg" in food_type and "non" not in food_type:
#             db_food_type = "Veg"
#         elif "non" in food_type:
#             db_food_type = "Non - Veg"
#         else:
#             raise HTTPException(status_code=400, detail="Unsupported food type")
        
#         logger.info(f"Converted food_type to: {db_food_type}")
        
#         if plan_type.lower() == "daily":
            
            
#             base_price = text("""
#             SELECT basic_price FROM meals 
#             WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
#             AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type)) 
#             AND num_people=:num_people 
#             AND LOWER(TRIM(basic_details))=LOWER(TRIM(:meal_type))
#         """)
            
#         # Get base price
#         base_query = text("""
#             SELECT basic_price FROM meals 
#             WHERE LOWER(TRIM(food_type))=LOWER(TRIM(:food_type)) 
#             AND LOWER(TRIM(plan_type))=LOWER(TRIM(:plan_type)) 
#             AND num_people=:num_people 
#             AND LOWER(TRIM(basic_details))=LOWER(TRIM(:meal_type))
#         """)
        
#         logger.info("Executing base price query with parameters:")
#         logger.info(f"food_type={db_food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}")
        
#         base_result = db.execute(base_query, {
#             "food_type": db_food_type,
#             "plan_type": plan_type,
#             "num_people": num_people,
#             "meal_type": meal_type
#         }).fetchone()
        
#         if not base_result:
#             logger.error("No matching meal plan found")
#             # raise HTTPException(
#             #     status_code=404,
#             #     detail=f"No meal plan found for food_type={db_food_type}, plan_type={plan_type}, num_people={num_people}, meal_type={meal_type}"
#             # )
#             return {"status" : "error", "message" : "missing or invalid parameters"}
        
#         base_price = base_result[0]
#         total = Decimal(str(base_price))
        
#         # Get additional services if any
#         if services:
#             # Convert services to a set to ensure uniqueness
#             unique_services = set(services)
            
#             placeholders = ', '.join([':service' + str(i) for i in range(len(unique_services))])
#             add_query = text(f"""
#                 SELECT DISTINCT ON (code) code, name, is_percentage, price_{num_people} as price 
#                 FROM additional_services 
#                 WHERE (
#                     LOWER(TRIM(food_type)) = LOWER(TRIM(:food_type))
#                     OR LOWER(TRIM(REPLACE(food_type, ' - ', '-'))) = LOWER(TRIM(:food_type))
#                     OR LOWER(TRIM(REPLACE(:food_type, ' - ', '-'))) = LOWER(TRIM(food_type))
#                     OR LOWER(TRIM(food_type)) = LOWER(TRIM(:normalized_food_type))
#                 )
#                 AND LOWER(TRIM(plan_type)) = LOWER(TRIM(:plan_type))
#                 AND code IN ({placeholders})
#                 ORDER BY code
#             """)
            
#             params = {
#                 "food_type": db_food_type,
#                 "normalized_food_type": db_food_type.replace(" - ", "-").replace(" -", "-").replace("- ", "-"),
#                 "plan_type": plan_type
#             }
#             params.update({f"service{i}": service for i, service in enumerate(unique_services)})
            
#             logger.info("Executing additional services query with parameters:")
#             logger.info(f"Query: {add_query}")
#             logger.info(f"Parameters: {params}")
            
#             results = db.execute(add_query, params).fetchall()
            
#             logger.info("Additional services found:")
#             # Track processed services to prevent duplicates
#             processed_services = set()
            
#             for code, name, is_percent, price in results:
#                 # Skip if we've already processed this service
#                 if code in processed_services:
#                     logger.info(f"Skipping duplicate service: {code}")
#                     continue
                    
#                 processed_services.add(code)
#                 logger.info(f"Service: {code} ({name})")
#                 logger.info(f"Is Percentage: {is_percent}")
#                 logger.info(f"Price: {price}")
                
#                 if is_percent:
#                     service_amount = (base_price * Decimal(str(price)) / Decimal('100'))
#                     logger.info(f"Percentage calculation: {base_price} * {price}% = {service_amount}")
#                     total += service_amount
#                 else:
#                     logger.info(f"Adding fixed amount: {price}")
#                     total += Decimal(str(price))
                
#                 logger.info(f"Running total: {total}")
        
#         response = {
#             "base_price": float(base_price),
#             "total_price": float(total),
#             "num_people": num_people,
#             "food_type": db_food_type,
#             "plan_type": plan_type,
#             "meal_type": meal_type,
#             "services": services
#         }
        
#         formatted_response = {
#             "status" : "success",
#             "message" : "packages fetched succesfully",
#             "packages" : {"package_type" : plan_type,
#                           "icon" : "Some icon bro",
#                           "package_id" : "STD6969",
#                           "price" : float(total)},
#             "features" : response   
#         }
        
#         logger.info("=== Response ===")
#         logger.info(json.dumps(response, indent=2))
        
#         return formatted_response
        
#     except Exception as e:
#         logger.error(f"Error in calculate_total: {str(e)}")
#         return {"status" : "error", "message" : "missing or invalid parameters"}



@router.get("/")
def calculate_total_cooking(
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

        food_type = food_type.strip().lower().replace(" ", "")
        if "veg" in food_type and "non" not in food_type:
            db_food_type = "Veg"
        elif "non" in food_type:
            db_food_type = "Non - Veg"
        else:
            raise HTTPException(status_code=400, detail="Unsupported food type")

        logger.info(f"Converted food_type to: {db_food_type}")

        # Determine applicable plan levels
        if plan_type.lower() == "daily":
            plan_levels = ["Standard", "Premium"]
        elif plan_type.lower() in ["weekly", "occasionally"]:
            plan_levels = ["Basic", "Standard", "Premium"]
        else:
            raise HTTPException(status_code=400, detail="Unsupported plan type")
        
        if "breakfast" in meal_type.lower() and "lunch" in meal_type.lower() and "dinner" in meal_type.lower():
            meal_type = "3 Meals {Breakfast+Tea & Lunch + Dinner}"   
        elif "breakfast" in meal_type.lower() and "lunch" in meal_type.lower():
            meal_type = "2 Meals {Breakfast+Tea & Lunch}"
        elif "lunch" in meal_type.lower():
            meal_type = "1 Meal Lunch"
        elif "dinner" in meal_type.lower():
            meal_type = "1 Meal Dinner"
        else:
            raise HTTPException (status_code= status.HTTP_404_NOT_FOUND, detail= "No such plan found bro")
        

        package_results = []

        for level in plan_levels:
            base_query = text("""
                SELECT basic_price FROM meals 
                WHERE LOWER(TRIM(food_type)) = LOWER(TRIM(:food_type)) 
                AND LOWER(TRIM(plan_type)) = LOWER(TRIM(:plan_type)) 
                AND num_people = :num_people 
                AND LOWER(TRIM(basic_details)) = LOWER(TRIM(:meal_type))
            """)

            logger.info("Executing base price query with parameters:")
            logger.info(f"food_type={db_food_type}, plan_type={level}, num_people={num_people}, meal_type={meal_type}")

            base_result = db.execute(base_query, {
                "food_type": db_food_type,
                "plan_type": level,
                "num_people": num_people,
                "meal_type": meal_type
            }).fetchone()

            if not base_result:
                logger.warning(f"No base price found for {level} plan")
                continue

            base_price = base_result[0]
            total = Decimal(str(base_price))

            # Handle additional services
            if services:
                unique_services = set(services)
                placeholders = ', '.join([f':service{i}' for i in range(len(unique_services))])
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
                    "plan_type": level
                }
                params.update({f"service{i}": s for i, s in enumerate(unique_services)})

                logger.info(f"Executing additional services query for {level} plan")
                results = db.execute(add_query, params).fetchall()

                processed_services = set()
                for code, name, is_percent, price in results:
                    if code in processed_services:
                        continue
                    processed_services.add(code)
                    if is_percent:
                        service_amount = (base_price * Decimal(str(price)) / Decimal('100'))
                        total += service_amount
                    else:
                        total += Decimal(str(price))

            package = {
                "package_type": level,
                "icon": "Some icon bro",
                "package_id": f"{level[:3].upper()}6969",
                "price": float(total)
            }

            features = {
                "base_price": float(base_price),
                "total_price": float(total),
                "num_people": num_people,
                "food_type": db_food_type,
                "plan_type": level,
                "meal_type": meal_type,
                "services": services
            }

            package_results.append({"package": package, "features": features})

        return {
            "status": "success",
            "message": "Packages fetched successfully",
            "results": package_results
        }

    except Exception as e:
        logger.error(f"Error in calculate_total: {str(e)}")
        return {"status": "error", "message": "missing or invalid parameters"}
