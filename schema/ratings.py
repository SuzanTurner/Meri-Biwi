from pydantic import BaseModel, ConfigDict
from typing import Optional

class Ratings(BaseModel):
    worker_id : int
    booking_id : int
    user_uid : str

    rating : int
    comments : Optional[str] = None

    model_config = ConfigDict(from_attributes = True)
    