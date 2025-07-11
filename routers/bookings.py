from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session
from modals.bookings import Booking, Cooking, Cleaning, CustomerAddress
from schema.bookings import GetBookings
import schemas



router = APIRouter(
    tags = ['Bookings'],
    prefix = '/bookings'
)


@router.get('/all', response_model=list[GetBookings])
async def get_all_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings

@router.post('/cooking')
async def book_cooking(request: schemas.CookingBooking, db: Session = Depends(get_db)):
    # Validate address_id
    address = db.query(CustomerAddress).filter(
        CustomerAddress.id == request.address_id,
        CustomerAddress.customer_id == request.customer_id
    ).first()
    if not address:
        return {
            "status": "error",
            "message": "Invalid address_id: address does not exist for this customer."
        }

    # Create Booking object
    booking = Booking(
        customer_id = request.customer_id,
        address_id = request.address_id,
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
        # latitude = request.latitude,
        # longitude = request.longitude,
        # city = request.city,
        # address_line_1 = request.address_line_1,
        # address_line_2 = request.address_line_2,
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
    # Validate address_id
    address = db.query(CustomerAddress).filter(
        CustomerAddress.id == request.address_id,
        CustomerAddress.customer_id == request.customer_id
    ).first()
    if not address:
        return {
            "status": "error",
            "message": "Invalid address_id: address does not exist for this customer."
        }

    # Create Booking object
    booking = Booking(
        customer_id = request.customer_id,
        address_id = request.address_id,
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
        # latitude = request.latitude,
        # longitude = request.longitude,
        # city = request.city,
        # address_line_1 = request.address_line_1,
        # address_line_2 = request.address_line_2,
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

@router.post('/address')
async def address(request: schemas.CreateBookingWithAddress, db: Session = Depends(get_db)):
    try:
        address = CustomerAddress(
            customer_id=request.customer_id,
            latitude = request.latitude,
            longitude = request.longitude,
            address_line1=request.address_line1,
            address_line2=request.address_line2,
            city=request.city,
            state=request.state,
            country=request.country,
            pincode=request.pincode,
            landmark=request.landmark,
            address_type=request.address_type,
            is_default=request.is_default
        )
        db.add(address)
        db.commit()
        db.refresh(address)

        return {
            "status": "success",
            "message": "Address added successfully",
            "address_id": address.id
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to add address.",
            "details": str(e)
        }
        
from fastapi import HTTPException

@router.put("/address")
async def update_address(request: schemas.CreateBookingWithAddress, address_id: int, db: Session = Depends(get_db)):
    address = db.query(CustomerAddress).filter(
        CustomerAddress.id == address_id,
        CustomerAddress.customer_id == request.customer_id
    ).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found for this customer.")

    # Update fields if provided
    address.address_line1 = request.address_line1 or address.address_line1
    address.address_line2 = request.address_line2 or address.address_line2
    address.latitude = request.latitude or address.latitude
    address.longitude = request.longitude or address.longitude
    address.city = request.city or address.city
    address.state = request.state or address.state
    address.country = request.country or address.country
    address.pincode = request.pincode or address.pincode
    address.landmark = request.landmark or address.landmark
    address.address_type = request.address_type or address.address_type
    address.is_default = request.is_default if request.is_default is not None else address.is_default

    try:
        db.commit()
        db.refresh(address)
        return {
            "status": "success",
            "message": "Address updated successfully",
            "address_id": address.id
        }
    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": "Failed to update address.",
            "details": str(e)
        }
    
        
@router.get('/{customer_id}')
async def my_bookings(customer_id: str, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.customer_id == customer_id).all()
    return {
        "status": "success",
        "data": [
            {
                "id" : booking.id,
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
                        "booking_id" : c.id,
                        "dietary_preference": c.dietary_preference,
                        "no_of_people": c.no_of_people,
                        "meals_per_day": c.meals_per_day,
                        "service_purpose": c.service_purpose,
                        "kitchen_platform_cleaning": c.kitchen_platform_cleaning,
                        "cooking_features" : [ f"Dietery Preference: {c.dietary_preference}",
                                                f"Service for {c.no_of_people} people",
                                                f"Meals per day: {c.meals_per_day}",
                                                "Service purpose: Daily",
                                                "Includes kitchen platform cleaning"],
                    }
                    for c in booking.cookings
                ],

                "cleaning_details": [
                    {
                        "booking_id" : cl.id,
                        "no_of_floors": cl.no_of_floors,
                        "no_of_bathrooms": cl.no_of_bathrooms,
                        "bhk": cl.bhk,
                        "plan": cl.plan,
                        "services": cl.services,
                        "cleaning_features" : ["Very amazing Features"],
                    }
                    for cl in booking.cleanings
                ],
 
                "address_details": {
                    "latitude": booking.address.latitude if booking.address else None,
                    "longitude": booking.address.longitude if booking.address else None,
                    "address_line_1": booking.address.address_line1 if booking.address else None,
                    "address_line_2": booking.address.address_line2 if booking.address else None,
                    "city": booking.address.city if booking.address else None,
                    "state": booking.address.state if booking.address else None,
                    "country": booking.address.country if booking.address else None,
                    "pincode": booking.address.pincode if booking.address else None,
                    "landmark": booking.address.landmark if booking.address else None,
                    "address_type": booking.address.address_type if booking.address else None,
                    "is_default": booking.address.is_default if booking.address else None,
                } if booking.address else None,
            }
            for booking in bookings
        ],
    }


@router.get('/{customer_id}/address')
async def my_addresses(customer_id: str, db: Session = Depends(get_db)):
    try:
        addresses = db.query(CustomerAddress).filter(CustomerAddress.customer_id == customer_id).all()
        return {"status" : "success",
            "address_data": [
                {   
                    "address_id" : address.id,
                    "latitude": address.latitude,
                    "longitude": address.longitude,
                    "address_line_1": address.address_line1,
                    "address_line_2": address.address_line2,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country,
                    "pincode": address.pincode,
                    "landmark": address.landmark,
                    "address_type": address.address_type,
                    "is_default": address.is_default
                }
                for address in addresses
            ]
        }
    except Exception as e:
        return {"status" : "error", "message" : "Address not fetched"}
    

@router.get('/all/')
async def get_all_bookings( db : Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings

