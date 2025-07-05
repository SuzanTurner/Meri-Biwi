from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class Ratings(BaseModel):
    worker_id : int
    booking_id : int
    user_uid : str

    rating : int
    comments : Optional[str] = None

    model_config = ConfigDict(from_attributes = True)

class RatingsResponse(BaseModel):
    rating: Optional[int]
    comments: Optional[str]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)