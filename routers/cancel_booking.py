from fastapi import APIRouter, Depends
from modals.bookings import Booking
from modals.refunds import Refund
from database import get_db
from sqlalchemy.orm import Session
from decimal import Decimal
import datetime

router = APIRouter(
    prefix  = '/cancellations',
    tags = ["Cancel Bookings"]
)

@router.post('/{id}')
async def cancel_booking(id : int, db : Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == id).first()
    if booking:

        booking.status = "cancelled"
        db.add(booking)

        # 2. Add refund row
        refund = Refund(
            booking_id=booking.id,
            customer_id=booking.customer_id,
            amount=booking.total_price or Decimal("0.00"),
            refund_status="pending",  # default
            payment_method="UPI",     # or pull this from Booking/Customer if available
            refund_date=datetime.datetime.now(),
        )
        db.add(refund)
        
        db.commit()
        return    {
            "status": "success",
            "message": "Booking cancelled successfully.",
            "data": {
                "booking_id": id,
                "refund_initiated": True,
                "cancellation_date": f"{datetime.datetime.now()}"
            }
        }
    return {
        "status": "error",
        "message": "Failed to cancel booking. Either booking not found or already completed."
        }

@router.post('refunds/{cid}')
async def refunds(cid : str, db : Session = Depends(get_db)):
    refund = db.query(Refund).filter(Refund.customer_id == cid).first()
    if refund:
        return {"status" : "success" , "data" : refund}
    return {"status" : "error", "message" : "No data found"}