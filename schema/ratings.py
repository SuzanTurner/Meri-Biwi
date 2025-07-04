from pydantic import BaseModel
from typing import Optional

class Ratings(BaseModel):
    id : int
    user_id : int
    rating : int
    review : Optional[str] = None