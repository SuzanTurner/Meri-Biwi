from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from modals.bookings import Booking
import datetime
import atexit
import asyncio

scheduler = BackgroundScheduler()

# day/month/year
# 2025-07-11 12:15:05.905244

# print(datetime.datetime.now())
# current_date = datetime.datetime.now()
# current_day = current_date.date()
# print(current_day)

async def check_date(db: Session = Depends(get_db)):
    current_day = datetime.date.today()
    bookings = db.query(Booking).filter(
        Booking.end_date == current_day,
        Booking.status != "Completed"
    ).all()

    # Update their status
    for booking in bookings:
        if booking.status != "Cancelled":
            booking.status = "Completed"  

    db.commit() 


def run_check_date():
    db = next(get_db())
    asyncio.run(check_date(db))

scheduler.add_job(
    run_check_date,
    trigger='cron',
    id='check_date',
    hour=0,
    minute=5
)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())


