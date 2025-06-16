from fastapi import APIRouter, Depends, Query, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from decimal import Decimal
import logging
import json

router = APIRouter(
    tags = ['Cleaning'],
    prefix = '/cleaning'
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/")
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

