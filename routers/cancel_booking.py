from fastapi import APIRouter, Depends
from modals.bookings import Booking
from modals.refunds import Refund
from database import get_db
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import datetime, timedelta

router = APIRouter(
    prefix  = '/cancellations',
    tags = ["Cancel Bookings"]
)

@router.post('/{id}')
async def cancel_booking(id : int, db : Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == id).first()
    if booking:

        booking.status = "Cancelled"
        booking.cancelled_at = datetime.now()
        db.add(booking)

        end = datetime.strptime(booking.end_date, "%d/%m/%Y")
        delta = end - datetime.now()

        # amount will be calculated:  per day charge= booking amount / frequency
        # refund amount = (remaining frequency days * per day charge) - 500rs(cancellation charges)
        per_day : float = booking.total_price / booking.freq

        amount : float = (delta.days * per_day) - 500

        # 2. Add refund row
        refund = Refund(
            booking_id=booking.id,
            customer_id=booking.customer_id,
            amount=amount,
            refund_status="pending",  
            payment_method="UPI",    
            refund_date=datetime.now(),
        )
        db.add(refund)
        
        db.commit()
        return    {
            "status": "success",
            "message": "Booking cancelled successfully.",
            "data": {
                "booking_id": id,
                "refund_initiated": True,
                "end_date" : booking.end_date,
                "delta" : delta.days,
                "per_day" : per_day,
                "refund_amount" : amount,
                "original_amount" : booking.total_price,
                "cancellation_date": f"{datetime.now()}"
            }
        }
    return {
        "status": "error",
        "message": "Failed to cancel booking. Either booking not found or already completed."
        }


@router.post('refunds/{cid}')
async def refunds(cid : str, db : Session = Depends(get_db)):
    refund = db.query(Refund).filter(Refund.customer_id == cid).all()
    if refund:
        return {"status" : "success" , "data" : refund}
    return {"status" : "error", "message" : "No data found"}