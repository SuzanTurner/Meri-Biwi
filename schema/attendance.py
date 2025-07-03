from pydantic import BaseModel, field_validator
import re
from typing import Optional

class Attendance(BaseModel):
    booking_id : int
    worker_id : int
    attendance_date : str
    status : bool
    checkin_time : Optional[str] = None
    checkout_time : Optional[str] = None
    notes : Optional[str] = None

    @field_validator("checkin_time", "checkout_time")
    def validate_time_format(cls, value):
        # Regex for HH:MM:SS (24-hour)
        if re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$", value) or re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", value):
            return value
