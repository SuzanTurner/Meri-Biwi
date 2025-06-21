from fastapi import APIRouter, Depends, Query
from database import get_db
from sqlalchemy.orm import Session
from modals.bookings import Booking, Cooking, Cleaning
import schemas


router = APIRouter(
    tags = ['Bookings'],
    prefix = '/bookings'
)

@router.post('/cooking')
async def book_cooking(request: schemas.CookingBooking, db: Session = Depends(get_db)):
    # Create Booking object
    booking = Booking(
        customer_id = request.customer_id,
        start_date = request.start_date,
        end_date = request.end_date,
        start_time = request.start_time,
        end_time = request.end_time,
        service_type = "cooking",
        worker_id_1 = request.worker_id_1,
        worker_id_2 = request.worker_id_2,
        package_id = request.package_id,
        basic_price = request.basic_price,
        total_price = request.total_price,
        status = getattr(request, 'status', 'ongoing')
    )

    # Create Cooking object
    cooking = Cooking(
        customer_id = request.customer_id,
        dietary_preference = request.dietary_preference,
        no_of_people = request.no_of_people,
        meals_per_day = request.meals_per_day,
        service_purpose = request.service_purpose,
        kitchen_platform_cleaning = request.kitchen_platform_cleaning,
        booking = booking
    )

    try:
        db.add(booking)
        db.add(cooking)
        db.commit()
        db.refresh(booking)
        db.refresh(cooking)

        return {
            "status": "success",
            "message": "Cooking service booked successfully",
            "data": {
                "booking_id": booking.id,
                "status": booking.status,
                "booking_date": booking.booking_date
            }
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to book Cooking Service.",
            "details": str(e)
        }


@router.post('/cleaning')
async def book_cleaning(request: schemas.CleaningBooking, db: Session = Depends(get_db)):
    # Create Booking object
    booking = Booking(
        customer_id = request.customer_id,
        start_date = request.start_date,
        end_date = request.end_date,
        start_time = request.start_time,
        end_time = request.end_time,
        service_type = "cleaning",
        worker_id_1 = request.worker_id_1,
        worker_id_2 = request.worker_id_2,
        package_id = request.package_id,
        basic_price = request.basic_price,
        total_price = request.total_price,
        status = getattr(request, 'status', 'ongoing')
    )

    # Create Cleaning object
    cleaning = Cleaning(
        customer_id = request.customer_id,
        no_of_floors = request.no_of_floors,
        no_of_bathrooms = request.no_of_bathrooms,
        bhk = request.bhk,
        plan = request.plan,
        services = request.services,
        booking = booking
    )

    try:
        db.add(booking)
        db.add(cleaning)
        db.commit()
        db.refresh(booking)
        db.refresh(cleaning)

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


@router.get('/')
async def my_bookings(customer_id: str, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.customer_id == customer_id).all()
    
    return {
        "status": "success",
        "data": [
            {
                "service_type": booking.service_type,
                "customer_id": booking.customer_id,
                "basic_price": float(booking.basic_price) if booking.basic_price else 0.0,
                "total_price": float(booking.total_price) if booking.total_price else 0.0,
                "start_date": booking.start_date,
                "end_date": booking.end_date,
                "start_time": booking.start_time,
                "end_time": booking.end_time,
                "booking_date": booking.booking_date,
                "worker_id_1": booking.worker_id_1,
                "worker_id_2": booking.worker_id_2,
                "status": booking.status,
                "package_id": booking.package_id,
                "cooking_details": [
                    {
                        "dietary_preference": c.dietary_preference,
                        "no_of_people": c.no_of_people,
                        "meals_per_day": c.meals_per_day,
                        "service_purpose": c.service_purpose,
                        "kitchen_platform_cleaning": c.kitchen_platform_cleaning,
                    }
                    for c in booking.cookings
                ],
                "cleaning_details": [
                    {
                        "no_of_floors": cl.no_of_floors,
                        "no_of_bathrooms": cl.no_of_bathrooms,
                        "bhk": cl.bhk,
                        "plan": cl.plan,
                        "services": cl.services,
                    }
                    for cl in booking.cleanings
                ]
            }
            for booking in bookings
        ]
    }

@router.get('/all/')
async def get_all_bookings( db : Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings
