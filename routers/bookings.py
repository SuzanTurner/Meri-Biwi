
from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.bookings import CustomerBooking
from datetime import datetime
from schemas import Booking


router = APIRouter(
    tags = ['Bookings'],
    prefix = '/book-cooking'
)

@router.post('/')
async def book_cooking(request: Booking, db: Session = Depends(get_db)):
    booking = CustomerBooking(
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
