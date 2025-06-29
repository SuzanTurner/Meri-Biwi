from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schema import attendance
from modals.attendance import Attendance

router = APIRouter(
    tags = ['Attendance'],
    prefix = '/attendance'
)

@router.post('/')
async def post_attendance(request : attendance.Attendance, db : Session = Depends(get_db)):
    try : 
        attendance = Attendance(
            booking_id = request.booking_id,
            worker_id = request.worker_id,
            attendance_date = request.attendance_date,
            status = request.status,
            checkin_time = request.checkin_time,
            checkout_time = request.checkout_time,
            notes = request.notes
        )

        db.add(attendance)
        db.commit()
        db.refresh(attendance)

        return {
            "success": True,
            "message": "Attendance recorded successfully",
            "attendance_id": attendance.id
            }
    except Exception:
        return {"status" : False,
                "message" : "Missing required fields"}
    
@router.put('/')
async def update_attendance(attendance_id : int, request : attendance.Attendance, db : Session = Depends(get_db)):
    try : 
        attends = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        attends.status = request.status
        attends.checkin_time = request.checkin_time
        attends.checkout_time = request.checkout_time
        attends.notes = request.notes
        db.commit()
        db.refresh(attends)
        return {
            "success": True,
            "message": "Attendance updated successfully"
            }
    
    except Exception:
        return {
            "success": False,
            "message": "Invalid attendance ID"
            }

@router.get('/')
async def get_attendance(booking_id : int, db : Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.booking_id == booking_id).first()
    return {"status" : "Success", "attendance" : attendance}
