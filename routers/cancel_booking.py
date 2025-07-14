from fastapi import APIRouter, Depends
from modals.bookings import Booking, Cooking, Cleaning
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
        if booking.freq == 30:
            amount : float = (delta.days * per_day) - 500

        else: 
            day : int = (delta.days / 7) * 2
            # amount : float = (per_day * day) - 500
            amount = (float(per_day) * day) - 500

        refund = Refund(
                booking_id=booking.id,
                customer_id=booking.customer_id,
                amount=max(0,amount),
                refund_status="pending",  
                payment_method="UPI", 
                # plan = booking.plan,   
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
                "start_date" : booking.start_date,
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


# @router.post('refunds/{cid}')
# async def refunds(cid : str, db : Session = Depends(get_db)):
#     refund = db.query(Refund).filter(Refund.customer_id == cid).all()
#     booking = db.query(Booking).filter(Booking.customer_id == cid).first()

#     plan_name = booking.service_type
#     if refund:
#         return {"status" : "success" , "plan_name" : plan_name, "data" : refund}
#     return {"status" : "error", "message" : "No data found"}


@router.post('/refunds/{cid}')
async def refunds(cid: str, db: Session = Depends(get_db)):
    refund_list = db.query(Refund).filter(Refund.customer_id == cid).all()
    booking = db.query(Booking).filter(Booking.customer_id == cid).first()

    if not refund_list or not booking:
        return {"status": "error", "message": "No data found"}
    
    if booking.service_type == "cooking":
        plan = db.query(Cooking).filter(Cooking.customer_id == cid).first()
        plan_name = f"{plan.plan} {booking.service_type} Plan".title()
    
    elif booking.service_type == "cleaning":
        plan = db.query(Cleaning).filter(Cleaning.customer_id == cid).first()
        plan_name = f"{plan.plan} {booking.service_type} Plan".title()

    # Serialize each refund and add plan_name
    # data = []
    # for refund in refund_list:
    #     r = refund.__dict__.copy()
    #     r.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal junk
    #     r["plan_name"] = plan_name
    #     r["plan_type"] = plan.plan
    #     r["service_purpose"] = plan.service_purpose
    #     data.append(r)

    data = []
    for refund in refund_list:
        r = refund.__dict__.copy()
        r.pop('_sa_instance_state', None)
        r["plan_name"] = plan_name
        r["plan_type"] = plan.plan
        r["service_purpose"] = plan.service_purpose
        # Optional: explicitly include refund_date if you’re unsure
        r["refund_date"] = refund.refund_date
        data.append(r)

    return {"status": "success", "data": data}
