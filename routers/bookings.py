
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.bookings import CookingBooking, CleaningBooking
from datetime import datetime
import schemas


router = APIRouter(
    tags = ['Bookings'],
    prefix = '/bookings'
)

@router.post('/cooking')
async def book_cooking(request: schemas.CookingBooking, db: Session = Depends(get_db)):
    booking = CookingBooking(
        customer_id = request.customer_id,
        dietary_preference = request.dietary_preference,
        no_of_people = request.no_of_people,
        meals_per_day = request.meals_per_day,
        service_purpose = request.service_purpose,
        kitchen_platform_cleaning = request.kitchen_platform_cleaning,
        start_date = request.start_date,
        end_date = request.end_date,
        start_time = request.start_time,
        end_time = request.end_time,
        worker_id_1 = request.worker_id_1,
        worker_id_2 = request.worker_id_2,
        package_id = request.package_id,
        basic_price = request.basic_price,
        total_price = request.total_price,
    )

    try:
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "message": "Cooking service booked successfully",
            "data": {
                "booking_id": booking.id,
                "status": "ongoing",
                "booking_date": datetime.now()
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to book Cooking Service.",
            "details": str(e)
        }


@router.post('/cleaning')
async def book_cleaning(request: schemas.CleaningBooking, db: Session = Depends(get_db)):
    booking = CleaningBooking(
        customer_id = request.customer_id,
        no_of_floors = request.no_of_floors,
        no_of_bathrooms = request.no_of_bathrooms,
        bhk = request.bhk,
        plan = request.plan,
        services = request.services,

        start_date = request.start_date,
        end_date = request.end_date,
        start_time = request.start_time,
        end_time = request.end_time,

        worker_id_1 = request.worker_id_1,
        worker_id_2 = request.worker_id_2,

        package_id = request.package_id,
        basic_price = request.basic_price,
        total_price = request.total_price,
        
        status = request.status
    )

    try:
        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {
            "status": "success",
            "message": "Cleaning service booked successfully",
            "data": {
                "booking_id": booking.id,
                "booking_date": booking.booking_date,
                "status": booking.status
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to book Cleaning Service.",
            "details": str(e)
        }
